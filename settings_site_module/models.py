from django.db import models

# Create your models here.


class HeaderSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    url_site = models.CharField(max_length=100, verbose_name='دامنه سایت')
    email = models.EmailField(max_length=100,null=True, blank=True ,verbose_name='ایمیل')
    is_main_setting = models.BooleanField(default=True, verbose_name='تنظیمات اصلی')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone_number = models.CharField(max_length=50, verbose_name='شماره تلفن')
    copy_right = models.CharField(max_length=200, null=True, blank=True, verbose_name='متن کپی رایت')
    site_logo = models.FileField(upload_to='images/site_settings', verbose_name='لوگوی سایت')
    image_about_us = models.ImageField(upload_to='images/about_us', null=True, blank=True, verbose_name='تصویر')
    title_history = models.CharField(max_length=200,null=True, blank=True, verbose_name='عنوان')
    text_history = models.TextField(null=True, blank=True, verbose_name='متن درباره ما')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیم هدر'
        verbose_name_plural = 'تنظیمات هدر سایت'

class AboutUs(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    text = models.TextField(null=True, blank=True, verbose_name='متن درباره ما')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'


class errosPicture(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    text = models.CharField(max_length=200, verbose_name='متن ارور')
    image = models.FileField(upload_to='images/errors_images', verbose_name='تصویر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تصویر خطا'
        verbose_name_plural = 'تصاویر خطاها'

class Footer(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان اصلی')

    class Meta:
        verbose_name = 'عنوان فوتر'
        verbose_name_plural = 'عناوین فوتر'
    def __str__(self):
        return self.title

class FooterItem(models.Model):
    title = models.CharField(max_length=150, verbose_name='آیتم هر عنوان در فوتر')
    url_title = models.CharField(max_length=150, verbose_name='عنوان در url')
    footer_main_title = models.ForeignKey(Footer,null=True, blank=True, on_delete=models.CASCADE, verbose_name='عنوان اصلی')

    class Meta:
        verbose_name = 'آیتم فوتر'
        verbose_name_plural = 'آیتم های فوتر'
    def __str__(self):
        return self.title
