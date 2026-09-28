from django import forms

from contact_us_module.models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'title', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full h-11 border border-gray-300 rounded-md  outline-none px-2 focus:border-gray-400 text-sm text-slate-700 transition-all ease-in duration-200 ',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full h-11 border border-gray-300 rounded-md  outline-none px-2 focus:border-gray-400 text-sm text-slate-700 transition-all ease-in duration-200 ',
                'required': 'required'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full h-11 border border-gray-300 rounded-md  outline-none px-2 focus:border-gray-400 text-sm text-slate-700 transition-all ease-in duration-200 ',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full  border py-2 border-gray-300 rounded-md resize-none outline-none px-2 focus:border-gray-400 text-sm text-slate-700 transition-all ease-in duration-200  ',
                'required': 'required',
                'row': 8
            }),
        }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'title': 'عنوان',
            'message': 'پیام',
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام نام خانوادگی خود را وارد کنید',
                'max_length': 'متن وارد شده بیش از حد مجاز می باشد'
            },
            'email': {
                'required': 'لطفاایمیل خود را وارد کنید',
                'max_length': 'متن وارد شده بیش از حد مجاز می باشد'
            },
            'title': {
                'required': 'لطفا عنوان پیام را وارد کنید',
                'max_length': 'متن وارد شده بیش از حد مجاز می باشد'
            },
            'message': {
                'required': 'لطفا متن پیام خود را وارد کنید',
                'max_length': 'متن وارد شده بیش از حد مجاز می باشد'
            },
        }

