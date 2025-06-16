from django.shortcuts import render, get_object_or_404, redirect
from .models import Master, Order

# Данные мастеров
MASTERS = [
    {'id': 1, 'name': 'Алексей Петров'},
    {'id': 2, 'name': 'Дмитрий Иванов'},
    {'id': 3, 'name': 'Сергей Сидоров'},
]

# Данные услуг
SERVICES = [
    'Мужская стрижка',
    'Стрижка бороды',
    'Укладка волос',
    'Мытье головы',
    'Массаж головы',
]

def landing(request):
    """Главная страница"""
    if request.method == 'POST':
        # Получаем данные из формы
        client_name = request.POST.get('name')
        phone = request.POST.get('phone')
        master_id = request.POST.get('master')
        service = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            # Сохраняем заявку в базу данных
            order = Order.objects.create(
                client_name=client_name or 'Не указано',
                phone=phone or 'Не указано',
                master_id=int(master_id) if master_id else 1,
                service=service or 'Не указано',
                date=date or 'Не указана',
                time=time or 'Не указано',
                status='новая'
            )
            
            # Перенаправляем на страницу благодарности
            return redirect('thanks')
            
        except Exception:
            # В случае ошибки остаемся на той же странице
            pass
    
    context = {
        'masters': MASTERS,
        'services': SERVICES,
    }
    return render(request, 'landing.html', context)


def thanks(request):
    """Страница благодарности"""
    return render(request, 'core/thanks.html')

def orders_list(request):
    """Список всех заявок"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Добавляем имена мастеров к заявкам
    for order in orders:
        for master in MASTERS:
            if master['id'] == order.master_id:
                order.master_name = master['name']
                break
        else:
            order.master_name = 'Неизвестный мастер'
        
        # Преобразуем услуги в список для шаблона
        order.services = [order.service]
    
    context = {
        'orders': orders,
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    """Детали конкретной заявки"""
    order = get_object_or_404(Order, id=order_id)
    
    # Находим мастера
    master = None
    for m in MASTERS:
        if m['id'] == order.master_id:
            master = m
            break
    
    # Преобразуем услуги в список для шаблона
    order.services = [order.service]
    
    context = {
        'order': order,
        'master': master,
    }
    return render(request, 'core/order_detail.html', context)
