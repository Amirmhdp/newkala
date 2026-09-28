from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from django.shortcuts import render, redirect
import requests
import json

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from account_module.models import Address, User
from order_module.models import Order, DetailOrder, Transaction
from product_module.models import Product


def add_product_to_order(request: HttpRequest):
    product_id = request.GET.get('product_id')
    print(f"product id is {product_id}")

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.detailorder_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += 1
                current_order_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول مورد نظر شما با موفقیت به سبدخرید اضافه شد',
                    'button': 'باشه ممنون',
                    'icon': 'success'
                })
            else:
                new_order_detail = DetailOrder(order_id=current_order.id, product_id=product_id, count=1)
                new_order_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول مورد نظر شما با موفقیت به سبدخرید اضافه شد',
                    'button': 'باشه ممنون',
                    'icon': 'success'

                })
        else:
            return JsonResponse({
                'status': 'not_found_product',
                'text': 'محصول مورد نظر شما یافت نشد',
                'button': 'باشه ممنون',
                'icon': 'error'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبدخرید می بایست ابتدا در سابت ثبت نام کنید',
            'button': 'ثبت نام',
            'icon': 'error'

        })

def _get_order_context(order):
    """محاسبه اطلاعات سبد خرید - قابل استفاده در هر دو view"""
    detail_order = (
        DetailOrder.objects
        .filter(order=order)
        .select_related('product')
        .order_by('-add_to_order_date')
    )

    total_price = sum(d.count * d.product.price for d in detail_order)
    total_price_with_discount = sum(d.count * d.product.final_price() for d in detail_order)

    return {
        'detail_order': detail_order,
        'detail_order_count': detail_order.count(),
        'total_price': total_price,
        'total_price_with_discount': total_price_with_discount,
        'discount': total_price - total_price_with_discount,
    }


def order(request: HttpRequest):
    order = (
        Order.objects
        .filter(user_id=request.user.id, is_paid=False)
        .first()
    )

    if not order:
        # سبد خرید خالی است
        return render(request, 'order_module/order_page.html', {
            'detail_order': [],
            'detail_order_count': 0,
            'total_price': 0,
            'total_price_with_discount': 0,
            'discount': 0,
            'newest_products': _get_newest_products(),
        })

    context = _get_order_context(order)
    context['newest_products'] = _get_newest_products()

    return render(request, 'order_module/order_page.html', context)


def change_count_product(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if state not in ('increase', 'decrease'):
        return JsonResponse({'error': 'invalid state'}, status=400)

    order = Order.objects.filter(user_id=request.user.id, is_paid=False).first()
    if not order:
        return JsonResponse({'error': 'order not found'}, status=404)

    detail_product = (
        DetailOrder.objects
        .select_related('product')
        .filter(id=detail_id, order=order)
        .first()
    )
    if not detail_product:
        return JsonResponse({'error': 'detail not found'}, status=404)

    if state == 'increase':
        detail_product.count += 1
        detail_product.save(update_fields=['count'])

    elif state == 'decrease':
        if detail_product.count <= 1:
            detail_product.delete()
        else:
            detail_product.count -= 1
            detail_product.save(update_fields=['count'])

    context = _get_order_context(order)
    data = render_to_string('order_module/component/order_page_ajax.html', context)

    return JsonResponse({'data_html': data})


def _get_newest_products():
    return (
        Product.objects
        .filter(is_delete=False, is_active=True)
        .order_by('-id')[:10]
    )




# ─────────────────────────────────────────────
# حالت تستی (Sandbox) — هیچ پول واقعی کم نمی‌شود
# وقتی به سرور واقعی رفتی، کافیست ZP_SANDBOX = False کنی
# ─────────────────────────────────────────────
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

# مهم: قبل از رفتن به سرور واقعی این مقدار را به دامنه واقعی سایت تغییر دهید
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
    errors = zp_response.get('errors')
    return bool(errors)


def _get_error_info(zp_response):
    errors = zp_response.get('errors') or {}
    if isinstance(errors, list):
        first = errors[0] if errors else {}
        return first.get('code', -1), first.get('message', 'خطای نامشخص')
    return errors.get('code', -1), errors.get('message', 'خطای نامشخص')


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    total_price = current_order.get_total_price()
    default_address = Address.objects.filter(user=request.user.id, is_default=True).first()
    if not default_address:
        messages.warning(request, "لطفا از منوی آدرس های من یک آدرس پیش فرض برای ارسال محصول انتخاب کنید")
        return redirect(reverse('user_panel_page'))
    if total_price <= 0:
        return redirect(reverse('order_page'))

    amount_toman = int(total_price) * 10

    metadata = {}
    raw_mobile = getattr(request.user, "number", None)
    mobile_str = str(raw_mobile) if raw_mobile else ''
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
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "خطا در اتصال به درگاه پرداخت",
            "message": message,
            "code": code,
            "sandbox": ZP_SANDBOX,
        })

    data = zp_response.get('data') or {}
    authority = data.get('authority')

    if not authority:
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "خطا در اتصال به درگاه پرداخت",
            "message": "پاسخ نامعتبر از درگاه دریافت شد.",
            "code": -1,
            "sandbox": ZP_SANDBOX,
        })

    if ZP_SANDBOX and not authority.startswith('S'):
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "خطای پیکربندی محیط تستی",
            "message": "این authority متعلق به محیط sandbox نیست. عملیات متوقف شد.",
            "sandbox": ZP_SANDBOX,
        })

    # ─── ساخت رکورد Transaction ───
    # توجه: authority باید unique باشد (طبق مدل شما). در حالت عادی هر بار
    # درخواست جدید authority جدید می‌دهد، پس مشکلی پیش نمی‌آید.
    Transaction.objects.create(
        order=current_order,
        authority=authority,
        amount=amount_toman,
        description=DESCRIPTION,
        email=request.user.email or '',
        mobile=mobile_str[:11],  # فیلد mobile در مدل شما max_length=11 دارد
    )

    return redirect(ZP_API_STARTPAY.format(authority=authority))


@login_required
def verify_payment(request: HttpRequest):
    t_authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if not t_authority:
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "درخواست نامعتبر",
            "message": "اطلاعات تراکنش یافت نشد.",
            "sandbox": ZP_SANDBOX,
        })

    transaction = Transaction.objects.filter(authority=t_authority).select_related('order').first()

    if not transaction:
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "سفارش یافت نشد",
            "message": "تراکنش پیدا نشد.",
            "sandbox": ZP_SANDBOX,
        })

    current_order = transaction.order

    if not current_order:
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "سفارش یافت نشد",
            "message": "سفارش مرتبط با این تراکنش پیدا نشد.",
            "sandbox": ZP_SANDBOX,
        })

    if status != 'OK':
        return render(request, 'order_module/payment_result_page.html', {
            "status": "canceled",
            "title": "تراکنش لغو شد",
            "message": "پرداخت توسط شما لغو شد یا انجام نشد.",
            "sandbox": ZP_SANDBOX,
        })

    amount_toman = int(transaction.amount)

    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount_toman,
        "authority": t_authority,
    }

    zp_response = _zp_post(ZP_API_VERIFY, req_data)

    if _has_error(zp_response):
        code, message = _get_error_info(zp_response)
        return render(request, 'order_module/payment_result_page.html', {
            "status": "error",
            "title": "خطا در تأیید پرداخت",
            "message": message,
            "code": code,
            "sandbox": ZP_SANDBOX,
        })

    data = zp_response.get('data') or {}
    t_status = data.get('code')
    ref_id = data.get('ref_id')


    if t_status == 100:

        for detail_item in current_order.detailorder_set.select_related('product'):
            detail_item.final_price = (
                    detail_item.count *
                    detail_item.product.final_price()
            )
            detail_item.save(update_fields=['final_price'])

        current_order.is_paid = True
        current_order.payment_date = timezone.now()

        current_order.save(
            update_fields=['is_paid', 'payment_date']
        )
        address = Address.objects.filter(user_id=request.user.id, is_default=True).first()
        transaction.is_paid = True
        transaction.reference_id = str(ref_id) if ref_id else None
        transaction.save(update_fields=['is_paid', 'reference_id'])
        phone_number = User.objects.filter(id=request.user.id).first()
        return render(request, 'order_module/payment_result_page.html', {
            "status": "success",
            "title": "پرداخت تستی با موفقیت انجام شد",
            "ref_id": ref_id,
            "amount": amount_toman,
            "order": current_order,
            "sandbox": ZP_SANDBOX,
            "address": address,
            "phone_number": phone_number,
        })

    elif t_status == 101:
        phone_number = User.objects.filter(id=request.user.id).first()
        address = Address.objects.filter(user_id=request.user.id, is_default=True).first()
        return render(request, 'order_module/payment_result_page.html', {
            "status": "success",
            "title": "این تراکنش قبلاً تأیید شده است",
            "message": data.get('message', ''),
            "ref_id": ref_id,
            "order": current_order,
            "sandbox": ZP_SANDBOX,
            "address": address,
            "phone_number": phone_number,
        })

    else:
        phone_number = User.objects.filter(id=request.user.id).first()
        address = Address.objects.filter(user_id=request.user.id, is_default=True).first()
        return render(request, 'order_module/payment_result_page.html', {
            "status": "failed",
            "title": "پرداخت ناموفق بود",
            "message": data.get('message', 'تراکنش با خطا مواجه شد.'),
            "sandbox": ZP_SANDBOX,
            "address": address,
            "phone_number": phone_number,
        })