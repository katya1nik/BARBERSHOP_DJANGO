from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Master, Service, Order, Review
from core.data import masters, services, orders
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Загружает начальные данные для барбершопа'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю загрузку начальных данных...')
        
        # Очищаем существующие данные
        self.stdout.write('Очищаю существующие данные...')
        Order.objects.all().delete()
        Review.objects.all().delete()
        Master.objects.all().delete()
        Service.objects.all().delete()
        
        # Создаем услуги
        self.stdout.write('Создаю услуги...')
        service_objects = []
        for service_name in services:
            service = Service.objects.create(
                name=service_name,
                description=f"Описание услуги: {service_name}",
                price=Decimal(str(random.randint(500, 3000))),
                duration=random.randint(30, 120),
                is_popular=random.choice([True, False])
            )
            service_objects.append(service)
            self.stdout.write(f'  - Создана услуга: {service.name}')
        
        # Создаем мастеров
        self.stdout.write('Создаю мастеров...')
        master_objects = []
        specializations = ['Парикмахер', 'Барбер', 'Стилист', 'Мастер по окрашиванию', 'Мастер по стрижке']
        
        for master_data in masters:
            master = Master.objects.create(
                name=master_data['name'],
                phone=f"+7{random.randint(9000000000, 9999999999)}",
                address=f"ул. Примерная, д. {random.randint(1, 100)}",
                experience=random.randint(1, 15),
                specialization=random.choice(specializations),
                is_active=True
            )
            
            # Добавляем случайные услуги мастеру
            master_services = random.sample(service_objects, random.randint(3, 6))
            master.services.set(master_services)
            
            master_objects.append(master)
            self.stdout.write(f'  - Создан мастер: {master.name}')
        
        # Создаем заказы
        self.stdout.write('Создаю заказы...')
        status_mapping = {
            'новая': 'pending',
            'подтвержденная': 'confirmed',
            'отмененная': 'cancelled',
            'выполненная': 'completed'
        }
        
        for order_data in orders:
            # Находим мастера по ID
            master = next((m for m in master_objects if m.id == order_data['master_id']), master_objects[0])
            
            # Находим услуги по названиям
            order_services = []
            for service_name in order_data['services']:
                service = next((s for s in service_objects if s.name == service_name), None)
                if service:
                    order_services.append(service)
            
            if not order_services:
                order_services = random.sample(service_objects, random.randint(1, 3))
            
            # Создаем заказ
            order = Order.objects.create(
                client_name=order_data['client_name'],
                phone=f"+7{random.randint(9000000000, 9999999999)}",
                comment=f"Комментарий к заказу: {order_data['client_name']}",
                status=status_mapping.get(order_data['status'], 'pending'),
                master=master,
                appointment_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30))
            )
            
            order.services.set(order_services)
            self.stdout.write(f'  - Создан заказ: {order.client_name}')
        
        # Создаем отзывы
        self.stdout.write('Создаю отзывы...')
        review_texts = [
            "Отличный мастер, очень доволен результатом!",
            "Профессионал своего дела, рекомендую всем.",
            "Хорошая работа, но можно было бы лучше.",
            "Прекрасный сервис, буду обращаться еще.",
            "Мастер знает свое дело, спасибо!",
            "Очень качественно выполнил работу.",
            "Доволен стрижкой, все аккуратно.",
            "Отличный результат, всем доволен.",
            "Хороший мастер, но дороговато.",
            "Профессионально и быстро."
        ]
        
        for master in master_objects:
            # Создаем 2-4 отзыва для каждого мастера
            for _ in range(random.randint(2, 4)):
                Review.objects.create(
                    client_name=f"Клиент {random.randint(1, 1000)}",
                    master=master,
                    rating=random.randint(3, 5),
                    text=random.choice(review_texts),
                    is_published=True
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Готово! Создано:\n'
                f'  - {len(service_objects)} услуг\n'
                f'  - {len(master_objects)} мастеров\n'
                f'  - {len(orders)} заказов\n'
                f'  - {Review.objects.count()} отзывов'
            )
        )


