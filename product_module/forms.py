from django import forms

from home_module.models import SearchHistory
from product_module.models import Comment


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'outline-none resize-none p-2 focus:border-gray-500 rounded transition-all duration-150 text-gray-800 text-sm border border-gray-400',
        'required': 'required',
        'placeholder': 'لطفا نظرات خود را با کاربران دیگر به اشتراک بگذارید'

    }),
        error_messages={
            'required': 'لطفا فرم کامنت را کامل کنید'
        }
    )
    comment_value = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'comment-value'}),
        required=False
    )

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','rating']
        widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'outline-none resize-none p-2 focus:border-gray-500 rounded transition-all duration-150 text-gray-800 text-sm border border-gray-400',
                'required': 'required',
                'placeholder': 'لطفا نظرات خود را با کاربران دیگر به اشتراک بگذارید'
            }),
            'comment_value': forms.HiddenInput(attrs={
                'id': 'comment-value'
            })

        }
        error_messages = {
            'comment': {
                'required': 'لطفا فرم کامنت را کامل کنید'
            }
        }

class SearchModelForm(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields = ['query']
        widgets = {
            'query': forms.TextInput(attrs={
                'name': "q",
                'required': 'required',
                'placeholder': 'جستجو در نیوکالا',
                'id': "search-box-md",
                'autocomplete': "off"

            }),


        }
