from django.shortcuts import render
from django.http import Http404
from .data import masters, services, orders

def landing(request):
    """Главная страница с мастерами и услугами"""
    context = {
        'masters': masters,
        'services': services
    }
    return render(request, 'landing.html', context)

def thanks(request):
    """Страница благодарности за заявку"""
    return render(request, 'core/thanks.html')

def orders_list(request):
    """Список всех заявок"""
    context = {
        'orders': orders
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    """Детальная информация о заявке"""
    # Находим заявку по ID
    order = None
    for o in orders:
        if o['id'] == order_id:
            order = o
            break
    
    if not order:
        raise Http404("Заявка не найдена")
    
    # Находим мастера по master_id
    master = None
    for m in masters:
        if m['id'] == order['master_id']:
            master = m
            break
    
    context = {
        'order': order,
        'master': master
    }
    return render(request, 'core/order_detail.html', context)

