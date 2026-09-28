from django.shortcuts import render
from settings_site_module.models import AboutUs,HeaderSettings
# Create your views here.



def about_us(request):
    image_about_us = HeaderSettings.objects.filter(is_main_setting=True).first()
    about_us_texts = AboutUs.objects.filter(is_active=True)

    context = {
        'image_about_us': image_about_us,
        'about_us_texts': about_us_texts
    }
    return render(request, 'settings_site_module/about_us.html', context)