from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Проверить структуру таблиц в базе данных'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Проверяем таблицу core_order
            cursor.execute("PRAGMA table_info(core_order)")
            columns = cursor.fetchall()
            
            self.stdout.write("Структура таблицы core_order:")
            for col in columns:
                self.stdout.write(f"  {col[1]} ({col[2]})")
            
            # Проверяем таблицу core_review
            cursor.execute("PRAGMA table_info(core_review)")
            columns = cursor.fetchall()
            
            self.stdout.write("\nСтруктура таблицы core_review:")
            for col in columns:
                self.stdout.write(f"  {col[1]} ({col[2]})")
