import csv
import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from recipes import models

CSV_DIR: Path = settings.BASE_DIR.parent / 'data'

TABLES = {
    models.Ingredient: {
        'path': 'ingredients.csv',
        'headers': (
            'name',
            'measurement_unit',
        ),
    },
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file in TABLES.items():
            with open(
                file=CSV_DIR / file['path'],
                encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(
                    csvfile,
                    fieldnames=file['headers']
                )
                try:
                    model.objects.bulk_create(
                        [model(**data) for data in reader],
                        ignore_conflicts=True
                    )
                except Exception as e:
                    print(e, file=sys.stderr)
                else:
                    self.stdout.write(
                        self.style.SUCCESS(_('Successfully fill in DB'))
                    )
