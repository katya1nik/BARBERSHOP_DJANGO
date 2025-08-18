from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
import os


class Master(models.Model):
    """Модель мастера барбершопа"""
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(
        upload_to="masters/",
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес", default="Не указан")
    experience = models.PositiveIntegerField(
        verbose_name="Стаж работы",
        help_text="Опыт работы в годах",
        default=0
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Специализация",
        help_text="Основная специализация мастера"
    )
    services = models.ManyToManyField(
        'Service',
        related_name="masters",
        verbose_name="Услуги"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            max_size = (400, 400)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(self.photo.path, optimize=True, quality=85)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"


class Service(models.Model):
    """Модель услуги барбершопа"""
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание услуги")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Длительность",
        help_text="Время выполнения в минутах"
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Order(models.Model):
    """Модель заказа клиента"""
    STATUS_CHOICES = [
        ('not_approved', 'Не подтвержден'),
        ('approved', 'Подтвержден'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="not_approved",
        verbose_name="Статус"
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Мастер"
    )
    # Временное поле для совместимости с базой данных
    # service = models.ForeignKey(
    #     Service,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     verbose_name="Услуга (временное)"
    # )
    services = models.ManyToManyField(
        Service,
        related_name="orders",
        verbose_name="Услуги"
    )

    def __str__(self) -> str:
        return f"Заказ {self.client_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Review(models.Model):
    """Модель отзыва о работе мастера"""
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    AI_CHOICES = [
        ("ai_checked_true", "Проверено ИИ"),
        ("ai_cancelled", "Отменено ИИ"),
        ("ai_checked_in_progress", "В процессе проверки"),
        ("ai_checked_false", "Не проверено"),
    ]

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name="Мастер"
    )
    photo = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")
    ai_checked_status = models.CharField(
        max_length=30,
        choices=AI_CHOICES,
        default="ai_checked_false",
        verbose_name="Статус ИИ",
    )

    def __str__(self) -> str:
        return f"Отзыв от {self.client_name} для {self.master.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
