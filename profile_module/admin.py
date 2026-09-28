from django.contrib import admin
from .models import Message
from settings_site_module.models import errosPicture
# Register your models here.

admin.site.register(Message)
admin.site.register(errosPicture)
