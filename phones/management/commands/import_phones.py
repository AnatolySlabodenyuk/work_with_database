import csv

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                phone, created = Phone.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'price': row['price'],
                        'image': row['image'],
                        'release_date': row['release_date'],
                        'lte_exists': row['lte_exists'].strip().lower() == 'true',
                        'slug': slugify(row['name']),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлен: {phone.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлён: {phone.name}'))
