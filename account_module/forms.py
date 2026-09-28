from django import forms
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):

    email = forms.EmailField(
        max_length=100,
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید'
        }
    )
    password = forms.CharField(
        max_length=100,
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا کلمه وارد کنید'
        }
    )
    confirm_password = forms.CharField(
        max_length=100,
        label=' تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا تکرار کلمه عبور وارد کنید'
        }

    )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')

class LoginForm(forms.Form):


    email = forms.EmailField(
        max_length=100,
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید'
        }
    )
    password = forms.CharField(
        max_length=100,
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا کلمه وارد کنید'
        }
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا ایمیل خود را وارد کنید'
        }
    )

class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        max_length=100,
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا کلمه وارد کنید'
        }
    )
    confirm_password = forms.CharField(
        max_length=100,
        label=' تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'w-[100%] px-2 py-2 text-gray-800 text-sm rounded outline-none border border-gray-300 focus:border-gray-500 transition-all duration-200 ease-in-out',
            'required': 'required'
        }),
        error_messages={
            'required': 'لطفا تکرار کلمه عبور وارد کنید'
        }

    )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')
