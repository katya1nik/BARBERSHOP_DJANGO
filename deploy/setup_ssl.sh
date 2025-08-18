#!/bin/bash

# Скрипт для настройки SSL сертификатов Let's Encrypt
# Использование: ./setup_ssl.sh yourdomain.com

set -e

DOMAIN=${1}
EMAIL="your-email@example.com"

if [ -z "$DOMAIN" ]; then
    echo "❌ Ошибка: Укажите домен"
    echo "Использование: ./setup_ssl.sh yourdomain.com"
    exit 1
fi

echo "🔒 Настраиваем SSL для домена: $DOMAIN"

# Устанавливаем certbot
echo "📦 Устанавливаем certbot..."
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Получаем SSL сертификат
echo "🎫 Получаем SSL сертификат..."
sudo certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive

# Настраиваем автоматическое обновление
echo "🔄 Настраиваем автоматическое обновление сертификатов..."
sudo crontab -l 2>/dev/null | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -

# Обновляем Django настройки
echo "⚙️ Обновляем Django настройки..."
sudo sed -i 's/SECURE_SSL_REDIRECT = False/SECURE_SSL_REDIRECT = True/' /path/to/your/project/barbershop/production_settings.py
sudo sed -i 's/SESSION_COOKIE_SECURE = False/SESSION_COOKIE_SECURE = True/' /path/to/your/project/barbershop/production_settings.py
sudo sed -i 's/CSRF_COOKIE_SECURE = False/CSRF_COOKIE_SECURE = True/' /path/to/your/project/barbershop/production_settings.py

# Перезапускаем сервисы
echo "🔄 Перезапускаем сервисы..."
sudo systemctl reload barbershop
sudo systemctl reload nginx

echo "🎉 SSL настройка завершена успешно!"
echo "🌐 Ваш сайт теперь доступен по HTTPS: https://$DOMAIN"
echo "🔄 Сертификаты будут автоматически обновляться каждый день в 12:00"
