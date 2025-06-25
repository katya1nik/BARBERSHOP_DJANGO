from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test

# Тестовые данные
MASTERS = [
    {'id': 1, 'name': 'Алексей Петров', 'specialization': 'Классические стрижки'},
    {'id': 2, 'name': 'Дмитрий Сидоров', 'specialization': 'Борода и усы'},
    {'id': 3, 'name': 'Михаил Иванов', 'specialization': 'Современные стрижки'},
]

SERVICES = [
    {'id': 1, 'name': 'Мужская стрижка', 'price': 800},
    {'id': 2, 'name': 'Стрижка бороды', 'price': 500},
    {'id': 3, 'name': 'Укладка', 'price': 300},
    {'id': 4, 'name': 'Комплекс', 'price': 1200},
]

ORDERS = [
    {
        'id': 1,
        'client_name': 'Иван Петров',
        'phone': '+7 (999) 123-45-67',
        'date': '2025-01-20',
        'time': '14:00',
        'services': ['Мужская стрижка', 'Стрижка бороды'],
        'master_id': 1,
        'status': 'новая',
        'comment': 'Хочу короткую стрижку'
    },
    {
        'id': 2,
        'client_name': 'Сергей Иванов',
        'phone': '+7 (999) 987-65-43',
        'date': '2025-01-21',
        'time': '16:30',
        'services': ['Комплекс'],
        'master_id': 2,
        'status': 'подтверждённая',
        'comment': ''
    },
    {
        'id': 3,
        'client_name': 'Андрей Сидоров',
        'phone': '+7 (999) 555-44-33',
        'date': '2025-01-22',
        'time': '12:00',
        'services': ['Мужская стрижка', 'Укладка'],
        'master_id': 3,
        'status': 'выполненная',
        'comment': 'Постоянный клиент'
    },
]

def landing(request):
    """Главная страница (лендинг)"""
    context = {
        'masters': MASTERS,
        'services': SERVICES,
    }
    return render(request, 'landing.html', context)

def thanks(request):
    """Страница благодарности за заявку"""
    return render(request, 'thanks.html')

def is_staff_user(user):
    """Проверка, является ли пользователь сотрудником"""
    return user.is_staff

@user_passes_test(is_staff_user)
def orders_list(request):
    """Список заявок (только для персонала)"""
    context = {
        'orders': ORDERS,
        'masters': MASTERS,
    }
    return render(request, 'orders_list.html', context)

@user_passes_test(is_staff_user)
def order_detail(request, order_id):
    """Детали заявки (только для персонала)"""
    # Находим заявку по ID
    order = None
    for o in ORDERS:
        if o['id'] == order_id:
            order = o
            break
    
    if not order:
        raise Http404("Заявка не найдена")
    
    # Находим мастера по ID
    master = None
    for m in MASTERS:
        if m['id'] == order['master_id']:
            master = m
            break
    
    context = {
        'order': order,
        'master': master,
        'services': SERVICES,
    }
    return render(request, 'order_detail.html', context)



