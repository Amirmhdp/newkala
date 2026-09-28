from django.db import models

# Create your models here.
from account_module.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    text = models.TextField(verbose_name='متن')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
    def __str__(self):
        return self.user.email
