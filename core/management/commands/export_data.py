from django.core.management.base import BaseCommand
from django.core import serializers
from core.models import Master, Service, Order, Review
from users.models import UserProfile
from django.contrib.auth.models import User
import json
import os

class Command(BaseCommand):
    help = 'Экспорт данных в JSON (UTF-8, читаемая кириллица), совместимый с loaddata'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='dump.json',
            help='Имя выходного файла'
        )

    def handle(self, *args, **options):
        output_file = options['output']

        # Формируем плоский список объектов в формате, совместимом с loaddata
        all_objects = []

        # Порядок важен из-за связей: сначала пользователи, затем профили и справочники
        all_objects.extend(serializers.serialize('python', User.objects.all()))
        all_objects.extend(serializers.serialize('python', UserProfile.objects.all()))
        all_objects.extend(serializers.serialize('python', Master.objects.all()))
        all_objects.extend(serializers.serialize('python', Service.objects.all()))
        all_objects.extend(serializers.serialize('python', Order.objects.all()))
        all_objects.extend(serializers.serialize('python', Review.objects.all()))

        # Сохраняем в файл с правильной кодировкой
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_objects, f, ensure_ascii=False, indent=2, default=str)

        self.stdout.write(self.style.SUCCESS(f'Данные успешно экспортированы в {output_file}'))
        try:
            self.stdout.write(f'Размер файла: {os.path.getsize(output_file)} байт')
        except OSError:
            pass
