#  IMPORTS
from functools import wraps

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from account_module.models import Address, City
from order_module.models import DetailOrder
from product_module.models import Favorite
from profile_module.forms import (
    AddressModelForm, AvatarModelForm, ProfileModelForm, ResetPasswordForm,
)
from profile_module.models import Message
from settings_site_module.models import errosPicture



#  HELPERS
VALID_STATUSES = {value for value, _ in DetailOrder.STATUS}


def ajax_login_required(view):
    """برای endpointهای AJAX: به‌جای redirect (که HTML صفحه‌ی لاگین را برمی‌گرداند) 401 می‌دهد."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'ابتدا وارد شوید'}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


def _get_data_filter(request):
    value = request.GET.get('data-filter', 'all')
    return value if value in VALID_STATUSES else 'all'


def _bought_items(user_id, status='all'):

    qs = (
        DetailOrder.objects
        .filter(order__user_id=user_id, order__is_paid=True)
        .select_related('product', 'order')
        .order_by('-order__payment_date', '-id')
    )
    if status != 'all':
        qs = qs.filter(status=status)
    return qs


def _favorites(user_id):
    """wishes.html از product.image / title_fa و final_price (⇒ discount) استفاده می‌کند."""
    return Favorite.objects.filter(user_id=user_id).select_related('product__discount')


# ═══════════════════════════════════════════════
#  USER PANEL
# ═══════════════════════════════════════════════
class UserPanelView(LoginRequiredMixin, View):
    login_url = 'login_page'
    template_name = 'profile_module/profile_page.html'

    def get_context_data(self, request, **kwargs):
        user = request.user
        data_filter = _get_data_filter(request)

        all_items = list(_bought_items(user.id, data_filter))

        if data_filter == 'all':
            recent_items = all_items[:4]
            bought_count = len(all_items)
        else:
            base = _bought_items(user.id)
            recent_items = list(base[:4])
            bought_count = base.count()

      
        user_comments = list(user.comment_set.select_related('product'))

        context = {
            'current_user': user,
            'count_bought_product': bought_count,
            'statuses': DetailOrder.STATUS,
            'data_filter': data_filter,
            'bought_products': recent_items,
            'all_bought_product': all_items,
            'get_addresses': Address.objects.filter(user_id=user.id),
            'favorite_products': _favorites(user.id),
            'profile_form': ProfileModelForm(instance=user),
            'avatar_form': AvatarModelForm(instance=user),
            'password_form': ResetPasswordForm(),
            'address': AddressModelForm(),
            'count_user_comment': len(user_comments),
            'user_comments': user_comments,
        }
        context.update(kwargs)
        return context

    def get(self, request):

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                'profile_module/component/order_list.html',
                {'all_bought_product': _bought_items(request.user.id, _get_data_filter(request))},
                request=request,
            )
            return JsonResponse({'html': html})

       
        return render(request, self.template_name, self.get_context_data(request))

    def post(self, request):
        handlers = {
            'edit_profile': self.edit_profile,
            'edit_avatar': self.edit_avatar,
            'change_password': self.change_password,
            'address': self.address,
            'edit_address': self.edit_address,
        }
        handler = handlers.get(request.POST.get('action'))
        if handler:
            return handler(request)
        return redirect('user_panel_page')

    # ─────────── پروفایل ───────────
    def edit_profile(self, request):
        form = ProfileModelForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات حساب کاربری با موفقیت تغییر کرد.')
            return redirect('user_panel_page')

        context = self.get_context_data(request, profile_form=form)
        return render(request, self.template_name, context)

    def edit_avatar(self, request):
        form = AvatarModelForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'عکس حساب کاربری با موفقیت تغییر کرد.')
            return redirect('user_panel_page')

        context = self.get_context_data(request, avatar_form=form)
        return render(request, self.template_name, context)

    def change_password(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['current_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save(update_fields=['password'])     
                update_session_auth_hash(request, user)
                messages.success(request, 'کلمه عبور با موفقیت تغییر کرد.')
                return redirect('user_panel_page')

            form.add_error('current_password', 'کلمه عبور فعلی صحیح نمی‌باشد.')

        context = self.get_context_data(request, password_form=form)
        return render(request, self.template_name, context)

    # ─────────── آدرس ───────────
    def address(self, request):
        form = AddressModelForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            with transaction.atomic():
                if form.cleaned_data.get('is_default'):
                    Address.objects.filter(user_id=request.user.id, is_default=True).update(is_default=False)
                address.save()

            messages.success(request, 'آدرس با موفقیت ثبت شد.')
            return redirect('user_panel_page')

        context = self.get_context_data(request, address=form)
        return render(request, self.template_name, context)

    def edit_address(self, request):
        instance = get_object_or_404(
            Address, id=request.POST.get('address_id') or 0, user=request.user
        )
        form = AddressModelForm(request.POST, instance=instance)
        if form.is_valid():
            address = form.save(commit=False)
            with transaction.atomic():
                if form.cleaned_data.get('is_default'):
                    (Address.objects
                     .filter(user_id=request.user.id, is_default=True)
                     .exclude(id=instance.id)
                     .update(is_default=False))
                address.save()

            messages.success(request, 'آدرس با موفقیت ویرایش شد.')
            return redirect('user_panel_page')

        context = self.get_context_data(request, address=form)
        return render(request, self.template_name, context)



#  AJAX ENDPOINTS
@ajax_login_required
def wishes_delete(request):
    wish_id = request.GET.get('wish-id', '')
    if wish_id.isdigit():
        Favorite.objects.filter(id=wish_id, user_id=request.user.id).delete()

    html = render_to_string(
        'profile_module/component/wishes.html',
        {'favorite_products': _favorites(request.user.id)},  
        request=request,
    )
    return JsonResponse({'html': html})


@ajax_login_required
def delete_address(request):
    address_id = request.GET.get('address-id', '')
    if address_id.isdigit():
        Address.objects.filter(id=address_id, user_id=request.user.id).delete()

    html = render_to_string(
        'profile_module/component/my_address.html',
        {'get_addresses': Address.objects.filter(user_id=request.user.id)},
        request,
    )
    return JsonResponse({'list_address': html})


@ajax_login_required
def load_cities(request):
    province_id = request.GET.get('province', '')

    address_form = AddressModelForm()
    address_form.fields['city'].queryset = (
        City.objects.filter(province_id=province_id)
        if province_id.isdigit() else City.objects.none()
    )

    html = render_to_string(
        'profile_module/component/cities_list.html',
        {'address': address_form},
        request=request,
    )
    return JsonResponse({'cities': html})



#  NOTIFICATIONS
class NotificationsView(LoginRequiredMixin, TemplateView):
    login_url = 'login_page'
    template_name = 'profile_module/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        notifications = list(
            Message.objects.filter(user_id=self.request.user.id).order_by('-id')
        )
        context['notifications'] = notifications    

        if not notifications:
            context['image_error'] = errosPicture.objects.filter(title='message').first()
        return context