from django.db import models

# Create your models here.
from account_module.models import User
from product_module.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده / نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def get_total_price(self):
        total = 0

        for item in self.detailorder_set.all():
            if self.is_paid:
                total += item.final_price or 0
            else:
                total += item.count * item.product.final_price()

        return total

    def __str__(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.email

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class DetailOrder(models.Model):
    STATUS = [
        ('paid', 'پرداخت شده'),
        ('delivered', 'تحویل داده شده'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='order_detail')
    add_to_order_date = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='تاریخ اضافه شدن به سبد خرید')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')
    status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default='paid', verbose_name='وضعیت محصول')

    def __str__(self):
        return self.product.title_fa

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'جزییات سبد خرید'


class Transaction(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='سبد خرید'
    )
    authority = models.CharField(max_length=255, unique=True)
    reference_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.TextField()
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=11, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"تراکنش سفارش #{self.order_id} - {self.order.user}"