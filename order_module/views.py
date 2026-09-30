import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.db.models import F
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from account_module.models import Address
from order_module.models import DetailOrder, Order, Transaction
from product_module.models import Product



#  Helpers
def _get_order_context(user_id):
    detail_order = list(
        DetailOrder.objects
        .filter(order__user_id=user_id, order__is_paid=False)
        .select_related('product__discount')
        .order_by('-add_to_order_date')
    )

    total_price = 0
    total_price_with_discount = 0
    for d in detail_order:
        total_price += d.count * d.product.price
        total_price_with_discount += d.count * d.product.final_price()

    return {
        'detail_order': detail_order,
        'detail_order_count': len(detail_order),  
        'total_price': total_price,
        'total_price_with_discount': total_price_with_discount,
        'discount': total_price - total_price_with_discount,
    }


def _get_newest_products():

    return (
        Product.objects
        .filter(is_delete=False, is_active=True)
        .select_related('discount')
        .order_by('-id')[:10]
    )



#  Cart
def add_product_to_order(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبدخرید می بایست ابتدا در سابت ثبت نام کنید',
            'button': 'ثبت نام',
            'icon': 'error',
        })

    product_id = request.GET.get('product_id', '')
    product_exists = product_id.isdigit() and Product.objects.filter(
        id=product_id, is_active=True, is_delete=False
    ).exists()                                 

    if not product_exists:
        return JsonResponse({
            'status': 'not_found_product',
            'text': 'محصول مورد نظر شما یافت نشد',
            'button': 'باشه ممنون',
            'icon': 'error',
        })

    current_order = Order.objects.filter(user_id=request.user.id, is_paid=False).first()
    if current_order is None:
        current_order = Order.objects.create(user_id=request.user.id)

    updated = (
        DetailOrder.objects
        .filter(order=current_order, product_id=product_id)
        .update(count=F('count') + 1)
    )
    if not updated:
        DetailOrder.objects.create(order=current_order, product_id=product_id, count=1)

    return JsonResponse({
        'status': 'success',
        'text': 'محصول مورد نظر شما با موفقیت به سبدخرید اضافه شد',
        'button': 'باشه ممنون',
        'icon': 'success',
    })


def order(request: HttpRequest):
    context = _get_order_context(request.user.id)  
    context['newest_products'] = _get_newest_products()
    return render(request, 'order_module/order_page.html', context)


def change_count_product(request: HttpRequest):
    state = request.GET.get('state')
    detail_id = request.GET.get('detail_id', '')

    if state not in ('increase', 'decrease'):
        return JsonResponse({'error': 'invalid state'}, status=400)
    if not detail_id.isdigit():
        return JsonResponse({'error': 'invalid detail_id'}, status=400)


    qs = DetailOrder.objects.filter(
        id=detail_id,
        order__user_id=request.user.id,
        order__is_paid=False,
    )

    if state == 'increase':
        changed = qs.update(count=F('count') + 1)
    else:
        changed = qs.filter(count__gt=1).update(count=F('count') - 1)
        if not changed:                       
            changed = qs.delete()[0]

    if not changed:
        return JsonResponse({'error': 'detail not found'}, status=404)

    context = _get_order_context(request.user.id)
    data = render_to_string('order_module/component/order_page_ajax.html', context)
    return JsonResponse({'data_html': data})



#  ZarinPal config
ZP_SANDBOX = True

if ZP_SANDBOX:
    MERCHANT = '12345678-1234-1234-1234-123456789012'
    ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
else:
    MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    ZP_API_REQUEST = "https://payment.zarinpal.com/pg/v4/payment/request.json"
    ZP_API_VERIFY = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
    ZP_API_STARTPAY = "https://payment.zarinpal.com/pg/StartPay/{authority}"

DESCRIPTION = "نهایی کردن خرید شما از سایت ما (حالت تستی)"
CALLBACK_URL = 'http://127.0.0.1:8000/order/verify-payment/'


def _zp_post(url, payload):
    headers = {"accept": "application/json", "content-type": "application/json"}
    try:
        resp = requests.post(url=url, data=json.dumps(payload), headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        try:
            body = e.response.text[:400] if e.response is not None else str(e)[:400]
        except Exception:
            body = str(e)[:400]
        return {"data": {}, "errors": {"code": -1, "message": f"خطای ارتباط با درگاه: {body}"}}
    except ValueError:
        return {"data": {}, "errors": {"code": -2, "message": "پاسخ سرور JSON معتبر نبود."}}


def _has_error(zp_response):
    return bool(zp_response.get('errors'))


def _get_error_info(zp_response):
    errors = zp_response.get('errors') or {}
    if isinstance(errors, list):
        first = errors[0] if errors else {}
        return first.get('code', -1), first.get('message', 'خطای نامشخص')
    return errors.get('code', -1), errors.get('message', 'خطای نامشخص')


def _error_page(request, title, message, **extra):
    return render(request, 'order_module/payment_result_page.html', {
        "status": "error", "title": title, "message": message,
        "sandbox": ZP_SANDBOX, **extra,
    })


def _success_page(request, **extra):
    """آدرس با ۱ کوئری؛ phone_number همان request.user است (بدون کوئری User)."""
    address = Address.objects.filter(user_id=request.user.id, is_default=True).first()
    return render(request, 'order_module/payment_result_page.html', {
        "status": "success",
        "sandbox": ZP_SANDBOX,
        "address": address,
        "phone_number": request.user,
        **extra,
    })



#  Request payment
@login_required
def request_payment(request: HttpRequest):
    # get_or_create ➜ filter().first(): دیگر سفارش خالی ساخته نمی‌شود
    current_order = Order.objects.filter(user=request.user, is_paid=False).first()
    if current_order is None:
        return redirect(reverse('order_page'))

    if not Address.objects.filter(user=request.user, is_default=True).exists():  # exists() به جای لود آبجکت
        messages.warning(request, "لطفا از منوی آدرس های من یک آدرس پیش فرض برای ارسال محصول انتخاب کنید")
        return redirect(reverse('user_panel_page'))

    total_price = current_order.get_total_price()   # حالا با ۱ کوئری JOIN
    if total_price <= 0:
        return redirect(reverse('order_page'))

    amount_toman = int(total_price) * 10

    metadata = {}
    mobile_str = str(getattr(request.user, "number", None) or '')
    if mobile_str:
        metadata["mobile"] = mobile_str
    if request.user.email:
        metadata["email"] = str(request.user.email)

    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount_toman,
        "callback_url": CALLBACK_URL,
        "description": DESCRIPTION,
    }
    if metadata:
        req_data["metadata"] = metadata

    zp_response = _zp_post(ZP_API_REQUEST, req_data)

    if _has_error(zp_response):
        code, message = _get_error_info(zp_response)
        return _error_page(request, "خطا در اتصال به درگاه پرداخت", message, code=code)

    authority = (zp_response.get('data') or {}).get('authority')
    if not authority:
        return _error_page(request, "خطا در اتصال به درگاه پرداخت",
                           "پاسخ نامعتبر از درگاه دریافت شد.", code=-1)

    if ZP_SANDBOX and not authority.startswith('S'):
        return _error_page(request, "خطای پیکربندی محیط تستی",
                           "این authority متعلق به محیط sandbox نیست. عملیات متوقف شد.")

    Transaction.objects.create(
        order=current_order,
        authority=authority,
        amount=amount_toman,
        description=DESCRIPTION,
        email=request.user.email or '',
        mobile=mobile_str[:11],
    )
    return redirect(ZP_API_STARTPAY.format(authority=authority))



#  Verify payment
@login_required
def verify_payment(request: HttpRequest):
    t_authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if not t_authority:
        return _error_page(request, "درخواست نامعتبر", "اطلاعات تراکنش یافت نشد.")

    txn = (
        Transaction.objects
        .filter(authority=t_authority, order__user=request.user)
        .select_related('order')
        .first()
    )
    if not txn:
        return _error_page(request, "سفارش یافت نشد", "تراکنش پیدا نشد.")

    current_order = txn.order      

    if status != 'OK':
        return render(request, 'order_module/payment_result_page.html', {
            "status": "canceled",
            "title": "تراکنش لغو شد",
            "message": "پرداخت توسط شما لغو شد یا انجام نشد.",
            "sandbox": ZP_SANDBOX,
        })

    if txn.is_paid:
        return _success_page(
            request,
            title="این تراکنش قبلاً تأیید شده است",
            ref_id=txn.reference_id,
            order=current_order,
        )

    amount_toman = int(txn.amount)
    zp_response = _zp_post(ZP_API_VERIFY, {
        "merchant_id": MERCHANT,
        "amount": amount_toman,
        "authority": t_authority,
    })

    if _has_error(zp_response):
        code, message = _get_error_info(zp_response)
        return _error_page(request, "خطا در تأیید پرداخت", message, code=code)

    data = zp_response.get('data') or {}
    t_status = data.get('code')
    ref_id = data.get('ref_id')

    if t_status == 100:
        with db_transaction.atomic():
            details = list(current_order.detailorder_set.select_related('product__discount'))
            for d in details:
                d.final_price = d.count * d.product.final_price()
            DetailOrder.objects.bulk_update(details, ['final_price'])  

            current_order.is_paid = True
            current_order.payment_date = timezone.now()
            current_order.save(update_fields=['is_paid', 'payment_date'])

            txn.is_paid = True
            txn.reference_id = str(ref_id) if ref_id else None
            txn.save(update_fields=['is_paid', 'reference_id'])

        return _success_page(
            request,
            title="پرداخت تستی با موفقیت انجام شد",
            ref_id=ref_id,
            amount=amount_toman,
            order=current_order,
        )

    if t_status == 101:
        return _success_page(
            request,
            title="این تراکنش قبلاً تأیید شده است",
            message=data.get('message', ''),
            ref_id=ref_id,
            order=current_order,
        )

    return render(request, 'order_module/payment_result_page.html', {
        "status": "failed",
        "title": "پرداخت ناموفق بود",
        "message": data.get('message', 'تراکنش با خطا مواجه شد.'),
        "sandbox": ZP_SANDBOX,
    })