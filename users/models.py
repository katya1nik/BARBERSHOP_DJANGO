from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    telegram_id = models.CharField(max_length=100, blank=True, verbose_name='Telegram ID')
    github_id = models.CharField(max_length=100, blank=True, verbose_name='GitHub ID')
    
    def __str__(self):
        return f'Профиль {self.user.username}'
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматически сохраняет профиль при сохранении пользователя"""
    try:
        # Проверяем, существует ли профиль
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # Если профиля нет, создаем его
            UserProfile.objects.get_or_create(user=instance)
    except UserProfile.DoesNotExist:
        # Если профиль не существует, создаем его
        UserProfile.objects.get_or_create(user=instance)
