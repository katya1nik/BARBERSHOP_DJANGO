from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Master(models.Model):
    """Модель мастера барбершопа"""
    name = models.CharField(max_length=100, verbose_name="Имя мастера")
    photo = models.ImageField(upload_to='masters/', verbose_name="Фото мастера")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Опыт работы (лет)")
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    services = models.ManyToManyField('Service', verbose_name="Услуги")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['name']

    def __str__(self):
        return self.name

class Service(models.Model):
    """Модель услуги барбершопа"""
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность (минуты)")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(blank=True, null=True, upload_to='services/', verbose_name="Изображение услуги")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']

    def __str__(self):
        return self.name

class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")
    services = models.ManyToManyField(Service, verbose_name="Услуги")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-date_created']

    def __str__(self):
        if self.appointment_date:
            return f"Заказ {self.client_name} - {self.appointment_date.strftime('%d.%m.%Y %H:%M')}"
        else:
            return f"Заказ {self.client_name} - Дата не указана"

class Review(models.Model):
    """Модель отзыва"""
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.client_name} - {self.rating}/5"