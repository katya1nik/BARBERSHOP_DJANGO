# Generated manually for UserProfile model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('telegram_id', models.CharField(blank=True, max_length=100, verbose_name='Telegram ID')),
                ('github_id', models.CharField(blank=True, max_length=100, verbose_name='GitHub ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]
