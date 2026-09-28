from django.contrib import messages
from django.shortcuts import render, redirect
from settings_site_module.models import HeaderSettings
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


from contact_us_module.forms import ContactUsForm


class ContactUsView(FormView):
    template_name = 'contact_us_module/contact_us_page.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('contact-us-page')
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'پیام شما با موفقیت ارسال گردید')
        return super(ContactUsView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data(**kwargs)
        site_settings = HeaderSettings.objects.filter(is_main_setting=True).first()
        context['site_settings'] = site_settings
        return context
        



# def ContactUsView(request):
#     return render(request, 'contact_us_module/contact_us_page.html')
