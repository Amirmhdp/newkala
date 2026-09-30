from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
from account_module.models import User


class Category(models.Model):
    main_category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE, verbose_name='دسته بندی اصلی')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='لینک')
    image = models.ImageField(upload_to='images/category',null=True, blank=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده /نشده')

    class Meta:
        verbose_name = 'دسته بندی اصلی'
        verbose_name_plural = 'دسته بندی های اصلی'
    def __str__(self):
        return self.title

class Product(models.Model):
    title_fa = models.CharField(max_length=250, verbose_name='نام فارسی محصول')
    title_en = models.CharField(max_length=250, null=True, blank=True ,verbose_name='نام انگلیسی محصول')
    url_title = models.SlugField(max_length=800, blank=True, db_index=True, unique=True, allow_unicode=True,verbose_name='لینک محصول')
    price = models.IntegerField(verbose_name='قیمت کالا')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True, verbose_name='برند', related_name='products')
    image = models.ImageField(upload_to='images/product', verbose_name='تصویر کالا')
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='تخفیف')
    is_amazing = models.BooleanField(default=False, verbose_name='محصول شگفت انگیز')
    category = models.ManyToManyField(Category, null=True, blank=True, verbose_name='دسته بندی')
    color = models.ManyToManyField('Color', null=True, blank=True, verbose_name='رنگ')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    description = models.TextField(null=True, blank=True, verbose_name='توضیح محصول')
    is_delete = models.BooleanField(default=False, verbose_name='حدف شده / نشده')

    @property
    def short_title_fa(self):
        return self.title_fa[:30] + ("..." if len(self.title_fa) > 30 else "")

    def final_price(self):
        if self.discount:
            return int(self.price - (self.price * self.discount.discount_value / 100))

        return int(self.price)
    def get_absolute_url(self):
        return reverse('product_detail_page', args=[self.url_title])
    def save(self, *args, **kwargs):
        self.url_title = slugify(self.title_fa, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title_fa

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
class Color(models.Model):
    color = models.CharField(max_length=100, verbose_name='رنک')
    url_title = models.CharField(max_length=100,null=True, blank=True, verbose_name='آدرس')
    colr_code = models.CharField(max_length=100, verbose_name='کد رنگی')
    is_active = models.BooleanField(default=True, verbose_name='کد رنگی')

    def __str__(self):
        return self.color
    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'


class Discount(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='عنوان تخفیف')
    discount_value = models.IntegerField( verbose_name='مقدار تخفیف')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='شروع تاریخ تخفیف')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='پایان تخفیف')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    duration_time = models.DurationField(default=timedelta(0), verbose_name="زمان باقی مانده")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیفات'


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان اسلایدر')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name='دسته بندی')
    brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.CASCADE, verbose_name='برند')
    image_sm = models.ImageField(null=True, blank=True, upload_to='images/slider', verbose_name='تصویر اسلایدر در اندازه موبایل')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='لینک')
    image_md = models.ImageField(null=True, blank=True, upload_to='images/slider', verbose_name='تصویر اسلایدر در انداره کامپیوتر')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان شروع')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان پایان')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سلایدر'
        verbose_name_plural = 'اسلایدر ها'

class Ads(models.Model):
    image = models.ImageField(upload_to='images/ads', null=True, blank=True, verbose_name='تصویر')
    url_title = models.SlugField(db_index=True, unique=True, verbose_name='لینک')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    def __str__(self):
        return self.url_title

    class Meta:
        verbose_name = 'تیلیغ'
        verbose_name_plural = 'تبلیغات'

class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=100, verbose_name='لینک')
    category = models.ManyToManyField('Category', null=True, blank=True, verbose_name='دسته بندی')
    is_active = models.BooleanField(default=True, verbose_name='فعال/ غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'


class SpecificationGroup(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='spec_groups',verbose_name='دسته بندی'
    )
    title = models.CharField(max_length=100,verbose_name='عنوان')

    class Meta:
        verbose_name = 'گروه مشخصات'
        verbose_name_plural = 'گروه مشخصات'

    def __str__(self):
        return self.title
class Attribute(models.Model):
    group = models.ForeignKey(
        SpecificationGroup,
        on_delete=models.CASCADE,
        related_name='attributes',verbose_name='گروه مشخصات دسته بندی'
    )

    title = models.CharField(max_length=100,verbose_name='عنوان مشخصات')

    class Meta:
        verbose_name = 'عنوان مشخصه'
        verbose_name_plural = 'عنوان مشخصات'

    def __str__(self):
        return self.title
class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications',verbose_name='محصول'
    )

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,verbose_name='عنوان مشخصات'
    )

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = 'ویژگی های محصول'
    def __str__(self):
        return self.attribute.title
class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name='values', verbose_name='محصول'
    )
    value = models.CharField(max_length=255, verbose_name='مشخصه محصول')
    class Meta:
        verbose_name = 'مشخصه'
        verbose_name_plural = 'مشخصات'

class Comment(models.Model):
    STATUS = [
        ('pending', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصولات')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    text = models.TextField(verbose_name='متن پیام')
    rating = models.IntegerField(null=True, blank=True, verbose_name='امتیاز', validators=[MinValueValidator(1),MaxValueValidator(5)], default=0 )
    updated_at = models.DateTimeField(auto_now=True , null=True, blank=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS,default='pending',blank=True, verbose_name='وضعیت کامنت')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)]) # رای از 1 تا 5
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name='rating_details') # لینک به کامنت، اختیاری

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.comment:
            if self.comment.product != self.product or self.comment.user != self.user:
                raise ValueError("کامنت ارائه شده به این رای تعلق ندارد.")
        super().save(*args, **kwargs)

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر محصول')

    def __str__(self):
        return self.product.title_fa
    class Meta:
        verbose_name = 'گالری محصول'
        verbose_name_plural = 'گالری محصولات'

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='محصول'
    )

    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ ایجاد'
    )

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = 'مورد علاقه'
        verbose_name_plural = 'مورد علاقه ها'
        unique_together = ['user', 'product']

