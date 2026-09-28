import json
import os
from django.core.management.base import BaseCommand
from account_module.models import Province


class Command(BaseCommand):
    help = "Import provinces into database"

    def handle(self, *args, **kwargs):

        file_path = os.path.join("data", "provinces.json")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found!"))
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.stdout.write("Starting import provinces...")

        for item in data:
            Province.objects.get_or_create(
                id=item["id"],
                name=item["name"]
            )

        self.stdout.write(self.style.SUCCESS("Provinces imported successfully!"))