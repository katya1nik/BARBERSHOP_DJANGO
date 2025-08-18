#!/bin/bash

# Скрипт для автоматического деплоя Django приложения
# Использование: ./deploy.sh [production|staging]

set -e

ENVIRONMENT=${1:-production}
PROJECT_DIR="/path/to/your/project"
VENV_DIR="$PROJECT_DIR/.venv"
BACKUP_DIR="$PROJECT_DIR/backups"

echo "🚀 Начинаем деплой в окружение: $ENVIRONMENT"

# Создаем резервную копию базы данных
echo "📦 Создаем резервную копию базы данных..."
mkdir -p "$BACKUP_DIR"
cp "$PROJECT_DIR/db.sqlite3" "$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"

# Активируем виртуальное окружение
echo "🐍 Активируем виртуальное окружение..."
source "$VENV_DIR/bin/activate"

# Переходим в директорию проекта
cd "$PROJECT_DIR"

# Получаем последние изменения из Git
echo "📥 Получаем последние изменения из Git..."
git pull origin main

# Устанавливаем/обновляем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt

# Применяем миграции
echo "🔄 Применяем миграции..."
python manage.py migrate

# Собираем статические файлы
echo "🎨 Собираем статические файлы..."
python manage.py collectstatic --noinput

# Проверяем конфигурацию
echo "✅ Проверяем конфигурацию Django..."
python manage.py check --deploy

# Перезапускаем сервисы
echo "🔄 Перезапускаем сервисы..."
sudo systemctl reload barbershop
sudo systemctl reload nginx

echo "🎉 Деплой завершен успешно!"
echo "📊 Статус сервисов:"
sudo systemctl status barbershop --no-pager -l
sudo systemctl status nginx --no-pager -l
