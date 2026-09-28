from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from utils.email_service import send_email
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html',context)
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email_entered = register_form.cleaned_data.get('email')

            password = register_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=email_entered).exists()
            if user:
                register_form.add_error('email','ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(
                    is_active=False,
                    active_account_code=get_random_string(72),
                    email=email_entered,
                    username=email_entered
                )

                new_user.set_password(password)
                new_user.save()
                send_email('فعال سازی حساب کاربری' , new_user.email, {'user': new_user}, 'email/email.html')
                return redirect(reverse('login_page'))
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html',context)

class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        context ={
            'login_form': login_form
        }
        return render(request,'account_module/login_page.html',context)

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            entered_email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email=entered_email).first()
            if user:
                if user.is_active:
                    is_correct_password = user.check_password(password)
                    if is_correct_password:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'ایمیل یا کلمه عبور وارد شده صحیح نمی باشد')
                else:
                    login_form.add_error('email', 'ایمیل یا کلمه عبور وارد شده صحیح نمی باشد')

            else:
                login_form.add_error('email','ایمیل یا کلمه عبور وارد شده صحیح نمی باشد')
        context = {
            'login_form': login_form
        }
        return render(request,'account_module/login_page.html',context)

class ActivateAccount(View):
    def get(self,request,email_active_code):
        user: User = User.objects.filter(active_account_code__iexact=email_active_code).first()
        if user:
            if not user.is_active:
                user.is_active = True
                user.active_account_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))

        else:
            return redirect(reverse('register_page'))

class ForgotPasswordView(View):
    def get(self,request):
        forgot_password_form = ForgotPasswordForm()
        context = {
            'forgot_password_form': forgot_password_form
        }
        return render(request, 'account_module/forgot_password.html', context)
    def post(self,request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            entered_email = forgot_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=entered_email).first()
            if user:
                send_email('بازیابی کلمه عبور',user.email, {'user': user}, 'email/reset_password.html')



            else:
                forgot_password_form.add_error('email', 'ایمیل وارد شده صجیج نمی باشد')
        context = {
            'forgot_password_form': forgot_password_form
        }
        return render(request, 'account_module/forgot_password.html', context)

class ResetPasswordView(View):
    def get(self, request, change_password_code):
        user: User = User.objects.filter(active_account_code__iexact=change_password_code).first()
        if user:
            reset_password_form = ResetPasswordForm()
            return render(request, 'account_module/reset_password_page.html', {
                'reset_password_form': reset_password_form
            })
        return redirect(reverse('forgot_password_page'))

    def post(self, request, change_password_code):
        reset_password_form = ResetPasswordForm(request.POST)

        if reset_password_form.is_valid():
            user: User = User.objects.filter(active_account_code__iexact=change_password_code).first()
            new_password = reset_password_form.cleaned_data.get('password')
            confirm_password = reset_password_form.cleaned_data.get('confirm_password')

            if not user:
                return redirect(reverse('register_page'))


            if new_password != confirm_password:
                reset_password_form.add_error('password', 'کلمه عبور با تکرار کلمه عبور مغایرت دارد')
            else:
                user.set_password(new_password)
                user.is_active = True
                user.active_account_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
        return render(request, 'account_module/reset_password_page.html', {
            'reset_password_form': reset_password_form
        })
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('home_page'))
