from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from account_module.models import User, Address, City
from order_module.models import DetailOrder, Order, Transaction
from product_module.models import Favorite
from profile_module.forms import ProfileModelForm, ResetPasswordForm, AvatarModelForm, AddressModelForm
from profile_module.models import Message
from settings_site_module.models import errosPicture



class UserPanelView(LoginRequiredMixin, View):
    login_url = 'login_page'
    template_name = 'profile_module/profile_page.html'

    def get_context_data(self, request, **kwargs):
        user = request.user
        count_bought_product = DetailOrder.objects.filter(order__user_id=user.id, order__is_paid=True).count()
        bought_product = DetailOrder.objects.filter(order__is_paid=True, order__user_id=user).order_by('-order__payment_date')[:4]
        all_bought_product = DetailOrder.objects.filter(order__is_paid=True, order__user_id=user).order_by('-order__payment_date')
        data_filter = request.GET.get('data-filter', 'all')
        if data_filter != 'all':
            all_bought_product = DetailOrder.objects.filter(order__is_paid=True, order__user_id=user, status=data_filter).order_by('-order__payment_date')
        get_addresses = Address.objects.filter(user_id=user)

        favorite_product = Favorite.objects.filter(user_id=request.user.id)
        print(favorite_product)
        context = {
            'current_user': user,
            'count_bought_product': count_bought_product,
            'statuses': DetailOrder.STATUS,
            'data_filter': data_filter,
            'bought_products': bought_product,
            'get_addresses': get_addresses,
            'favorite_products': favorite_product,
            'all_bought_product': all_bought_product,
            'profile_form': ProfileModelForm(instance=user),
            'avatar_form': AvatarModelForm(instance=user),
            'password_form': ResetPasswordForm(),
            'address': AddressModelForm(),
            'count_user_comment': user.comment_set.count(),
            'user_comments': user.comment_set.all(),

        }
        context.update(kwargs)
        return context

    def get(self, request):
        context = self.get_context_data(request)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                'profile_module/component/order_list.html',
                context,
                request=request
            )
            return JsonResponse({
                'html': html
            })
        return render(request, 'profile_module/profile_page.html', self.get_context_data(request))

    def post(self, request):

        action = request.POST.get('action')

        handlers = {
            'edit_profile': self.edit_profile,
            'edit_avatar': self.edit_avatar,
            'change_password': self.change_password,
            'address': self.address,
            'edit_address': self.edit_address,
        }
        handler = handlers.get(action)
        if handler:
            return handler(request)
        return redirect('user_panel_page')


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
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'کلمه عبور با موفقیت تغییر کرد.')
                return redirect('user_panel_page')

            form.add_error('current_password', 'کلمه عبور فعلی صحیح نمی‌باشد.')

        context = self.get_context_data(request, password_form=form)
        return render(request, self.template_name, context)

    def address(self, request):
        form = AddressModelForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if form.cleaned_data.get('is_default'):
                Address.objects.filter(is_default=True, user_id=request.user).update(is_default=False)
            address.save()

            messages.success(request, 'آدرس با موفقیت ثبت شد.')
            return redirect('user_panel_page')

        context = self.get_context_data(request, address=form)
        return render(request, self.template_name, context)

    def edit_address(self, request):
        from django.shortcuts import get_object_or_404
        address_id = request.POST.get('address_id')
        instance = get_object_or_404(Address, id=address_id, user=request.user)
        form = AddressModelForm(request.POST, instance=instance)

        if form.is_valid():
            address = form.save(commit=False)
            if form.cleaned_data.get('is_default'):
                Address.objects.filter(is_default=True, user_id=request.user).exclude(id=address_id).update(is_default=False)
            address.save()
            messages.success(request, 'آدرس با موفقیت ویرایش شد.')
            return redirect('user_panel_page')

        context = self.get_context_data(request, address=form)
        return render(request, self.template_name, context)

def wishes_delete(request):
    wishes_id = request.GET.get('wish-id')
    print(wishes_id)
    Favorite.objects.filter(id=wishes_id, user_id=request.user.id).delete()
    favorite_products = Favorite.objects.filter(user_id=request.user.id)
    context = {
        "favorite_products": favorite_products
    }
    html = render_to_string('profile_module/component/wishes.html',context, request=request)
    return JsonResponse({
        'html': html
    })

def delete_address(request):

    address_id = request.GET.get('address-id')
    Address.objects.filter(id=address_id).delete()
    get_addresses = Address.objects.filter(user_id=request.user.id)
    context = {
        'get_addresses': get_addresses
    }
    html = render_to_string('profile_module/component/my_address.html', context, request)

    return JsonResponse({
        'list_address': html
    })

def load_cities(request):
    province_id = request.GET.get('province')

    address_form = AddressModelForm()
    address_form.fields['city'].queryset = City.objects.filter(
        province_id=province_id
    )

    html = render_to_string(
        'profile_module/component/cities_list.html',
        {
            'address': address_form
        },
        request=request
    )

    return JsonResponse({
        'cities': html
    })

class NotificationsView(TemplateView):
    template_name = 'profile_module/notifications.html'

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        request: HttpRequest = self.request
        messages = Message.objects.filter(user_id=request.user.id).order_by('-id')
        image_error = errosPicture.objects.filter(title='message').first()
        context['messages'] = messages
        context['image_error'] = image_error
        return context