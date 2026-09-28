from django.db import models

from account_module.models import User


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کارب')
    query = models.CharField(max_length=200, verbose_name='متن جستجو شده')
    created_at = models.DateTimeField(auto_now=True, verbose_name='زمان سرچ')

    class Meta:
        verbose_name = 'تاریخ جستجو'
        verbose_name_plural = 'تاریخچه جستجوها'
    def __str__(self):
        return self.query