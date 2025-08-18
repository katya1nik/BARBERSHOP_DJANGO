# 🚀 Инструкция по деплою Django приложения

## 📋 Требования

- Ubuntu 20.04+ или CentOS 7+
- Python 3.11+
- Nginx
- Git
- SSH доступ к серверу

## 🛠️ Установка на сервере

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка Python и зависимостей
```bash
sudo apt install -y python3 python3-pip python3-venv nginx git
```

### 3. Создание пользователя для приложения
```bash
sudo adduser www-data
sudo usermod -aG sudo www-data
```

### 4. Клонирование проекта
```bash
cd /var/www/
sudo git clone https://github.com/yourusername/barbershop.git
sudo chown -R www-data:www-data barbershop
```

### 5. Настройка виртуального окружения
```bash
cd barbershop
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install -r requirements.txt
sudo -u www-data .venv/bin/pip install gunicorn
```

### 6. Настройка переменных окружения
```bash
sudo -u www-data cp env.example .env
sudo -u www-data nano .env
```

## ⚙️ Конфигурация

### 1. Настройка Nginx
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/barbershop
sudo ln -s /etc/nginx/sites-available/barbershop /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 2. Настройка Gunicorn
```bash
sudo cp deploy/barbershop.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable barbershop
sudo systemctl start barbershop
```

### 3. Настройка базы данных
```bash
sudo -u www-data .venv/bin/python manage.py migrate
sudo -u www-data .venv/bin/python manage.py collectstatic --noinput
```

## 🔒 Настройка SSL

### 1. Автоматическая настройка
```bash
cd deploy
chmod +x setup_ssl.sh
./setup_ssl.sh yourdomain.com
```

### 2. Ручная настройка
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 🚀 Автоматический деплой

### 1. Настройка GitHub Secrets
Добавьте в настройки репозитория:
- `HOST` - IP адрес сервера
- `USERNAME` - имя пользователя
- `SSH_KEY` - приватный SSH ключ

### 2. Запуск деплоя
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh production
```

## 📊 Мониторинг

### 1. Статус сервисов
```bash
sudo systemctl status barbershop
sudo systemctl status nginx
```

### 2. Логи
```bash
sudo journalctl -u barbershop -f
sudo tail -f /var/log/nginx/error.log
```

## 🔧 Устранение неполадок

### 1. Проверка конфигурации Django
```bash
sudo -u www-data .venv/bin/python manage.py check --deploy
```

### 2. Проверка прав доступа
```bash
sudo chown -R www-data:www-data /var/www/barbershop
sudo chmod -R 755 /var/www/barbershop
```

### 3. Перезапуск сервисов
```bash
sudo systemctl restart barbershop
sudo systemctl restart nginx
```

## 📝 Полезные команды

```bash
# Обновление сертификатов
sudo certbot renew

# Проверка SSL
curl -I https://yourdomain.com

# Мониторинг ресурсов
htop
df -h
free -h
```

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи сервисов
2. Убедитесь в правильности конфигурации
3. Проверьте права доступа к файлам
4. Убедитесь в доступности портов 80 и 443
