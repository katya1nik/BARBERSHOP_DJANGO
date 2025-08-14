from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создает суперпользователя если его нет'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Суперпользователь уже существует')
            return
        
        username = 'admin'
        email = 'admin@barbershop.com'
        password = 'admin123'
        
        try:
            user = User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Суперпользователь создан:\n'
                    f'  Username: {username}\n'
                    f'  Email: {email}\n'
                    f'  Password: {password}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании суперпользователя: {e}')
            )


