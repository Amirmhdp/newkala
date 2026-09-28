import json
import os
import requests
from django.core.management.base import BaseCommand
from account_module.models import City, Province


class Command(BaseCommand):
    help = "Import Iran cities"

    def handle(self, *args, **kwargs):

        url = "https://raw.githubusercontent.com/jd1378/iran-cities-json/master/shahr.json"
        data = requests.get(url).json()

        self.stdout.write("Starting import cities...")

        for item in data:
            city_name = item.get("name")
            province_id = item.get("ostan")

            if not city_name or not province_id:
                continue

            try:
                province = Province.objects.get(id=province_id)
            except Province.DoesNotExist:
                continue

            City.objects.get_or_create(
                name=city_name,
                province=province
            )

        self.stdout.write(self.style.SUCCESS("Cities imported successfully!"))