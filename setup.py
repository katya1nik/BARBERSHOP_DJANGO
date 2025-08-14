#!/usr/bin/env python3
"""
Скрипт для быстрой настройки проекта Барбершоп
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} выполнено успешно")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description.lower()}:")
        print(f"Команда: {command}")
        print(f"Ошибка: {e.stderr}")
        return False

def main():
    """Основная функция настройки"""
    print("🚀 Настройка проекта Барбершоп Django")
    print("=" * 50)
    
    # Проверяем, что мы в правильной директории
    if not Path("manage.py").exists():
        print("❌ Ошибка: файл manage.py не найден!")
        print("Запустите скрипт из корневой директории проекта")
        sys.exit(1)
    
    # Устанавливаем переменную окружения Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
    
    # Применяем миграции
    if not run_command("python manage.py migrate", "Применение миграций"):
        sys.exit(1)
    
    # Загружаем начальные данные
    if not run_command("python manage.py load_initial_data", "Загрузка начальных данных"):
        sys.exit(1)
    
    # Создаем суперпользователя
    if not run_command("python manage.py create_superuser", "Создание суперпользователя"):
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Настройка завершена успешно!")
    print("\n📋 Что было создано:")
    print("  • Применены миграции базы данных")
    print("  • Загружены начальные данные (мастера, услуги, заказы)")
    print("  • Создан суперпользователь (admin/admin123)")
    print("\n🚀 Для запуска сервера выполните:")
    print("  python manage.py runserver")
    print("\n🔐 Для входа в админку:")
    print("  URL: http://127.0.0.1:8000/admin/")
    print("  Логин: admin")
    print("  Пароль: admin123")

if __name__ == "__main__":
    main()


