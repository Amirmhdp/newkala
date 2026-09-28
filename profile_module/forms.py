from django import forms
# فرض می‌کنیم مدل شما UserProfile نام دارد
# from .models import UserProfile
from django.core.exceptions import ValidationError

from account_module.models import User, Address
import jdatetime

from django import forms
from account_module.models import User


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name','birthday','gender','first_name','last_name','meli_code', 'about_user', 'number']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'number': forms.TextInput(),
            'email': forms.EmailInput(),

            'full_name': forms.TextInput(),
            'meli_code': forms.TextInput(attrs={
                'placeholder': '1234567890'
            }),
            'birthday': forms.TextInput(attrs={
                'placeholder': '1234567890',
                'id': 'birthday-input'
            }),
            'about_user': forms.Textarea(attrs={
                'rows': 4
            }),

        }
class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['province', 'city', 'mobile', 'title', 'postal_code', 'full_address', 'is_default', 'receiver_name']
        widgets = {
            'mobile': forms.TextInput(attrs={
                'placeholder': "09xxxxxxxxx"
            }),
            'postal_code': forms.TextInput(attrs={
                'placeholder': '۱۰ رقم'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'منزل'
            }),
            'receiver_name': forms.TextInput(attrs={
                'placeholder': 'نام گیرنده'
            }),
            'full_address': forms.Textarea(attrs={
                'class': 'full'
            }),
        }
class AvatarModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'hidden'
            })
        }
class ResetPasswordForm(forms.Form):

    current_password = forms.CharField(
        max_length=100,
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'required': 'required',
            'placeholder': '........',
            'onfocus': "this.style.borderColor='var(--red)'",
            'onblur': "this.style.borderColor='var(--border)'"
        }),
        error_messages={
            'required': 'لطفا کلمه وارد کنید'
        }
    )
    new_password = forms.CharField(
        max_length=100,
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'required': 'required',
            'placeholder': '........',
            'onfocus': "this.style.borderColor='var(--red)'",
            'onblur': "this.style.borderColor='var(--border)'"
        }),
        error_messages={
            'required': 'لطفا کلمه وارد کنید'
        }
    )
    confirm_new_password = forms.CharField(
        max_length=100,
        label=' تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'required': 'required',
            'placeholder': '........',
            'onfocus': "this.style.borderColor='var(--red)'",
            'onblur': "this.style.borderColor='var(--border)'"
        }),
        error_messages={
            'required': 'لطفا تکرار کلمه عبور وارد کنید'
        }

    )
    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password == confirm_new_password:
            return confirm_new_password
        else:
            raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')