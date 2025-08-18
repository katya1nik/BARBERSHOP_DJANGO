from django.core.management.base import BaseCommand
from core.models import Review


class Command(BaseCommand):
    help = 'Проверить отзывы в базе данных'

    def handle(self, *args, **options):
        reviews = Review.objects.all()
        self.stdout.write(f"Всего отзывов в базе: {reviews.count()}")
        
        if reviews.exists():
            self.stdout.write("Отзывы:")
            for review in reviews:
                self.stdout.write(f"  ID {review.id}: {review.client_name} - {review.text[:50]}...")
        else:
            self.stdout.write("Отзывов в базе нет!")
