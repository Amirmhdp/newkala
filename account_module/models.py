from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
        ('other', "ترجیح میدهم نگویم")
    ]
    email = models.EmailField(max_length=100,verbose_name='ایمیل')
    full_name = models.CharField(max_length=100, blank=True, null=True,verbose_name='نام و نام خانوادگی')
    meli_code = models.CharField(null=True, blank=True,max_length=10, verbose_name='کد ملی')
    city = models.CharField(null=True, blank=True,max_length=200, verbose_name='شهر')
    about_user = models.TextField(null=True, blank=True,verbose_name='درباره کاربر')
    birthday = models.DateField(null=True, blank=True,verbose_name='تاریخ تولد')
    avatar = models.ImageField(upload_to='images/avatar', null=True, blank=True, verbose_name='تصویر کاربر')
    active_account_code = models.CharField(max_length=72, verbose_name='کد فعال سازی')
    number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='شماره همراه باید با 09 شروع شده و ۱۱ رقم باشد.'
            )
        ],
        verbose_name='شماره تلفن'
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True, blank=True, verbose_name='جنسیت')

    def __str__(self):
        full_name = self.get_full_name()

        if full_name:
            return f"{full_name} - {self.id}"

        return f"کاربر نیوکالا"

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name='استان')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان ها'


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities',verbose_name='استان')
    name = models.CharField(max_length=100, verbose_name='شهر')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='address')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='استان')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='شهر')
    postal_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='کد پستی باید دقیقا ۱۰ رقم باشد.'
            )
        ],
        verbose_name='کد پستی'
    )

    mobile = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='شماره همراه باید با 09 شروع شده و ۱۱ رقم باشد.'
            )
        ],
        verbose_name='شماره تلفن'
    )
    full_address = models.TextField(verbose_name='آدرس کامل')
    receiver_name = models.CharField(
        max_length=100,
        verbose_name='نام گیرنده',

    )
    is_default = models.BooleanField(default=False, verbose_name='آدرس پیش فرض')
    title = models.CharField(max_length=100, verbose_name='عنوان آدرس')


    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'


