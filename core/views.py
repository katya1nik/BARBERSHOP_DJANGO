from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from core.models import Master, Service, Order, Review

def is_staff_user(user):
    """Проверка, является ли пользователь сотрудником"""
    return user.is_staff

def landing(request):
    """Главная страница с формой записи"""
    if request.method == 'POST':
        # Получаем данные из формы
        client_name = request.POST.get('client_name')
        phone = request.POST.get('phone')
        master_id = request.POST.get('master')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        comment = request.POST.get('comment')
        services = request.POST.getlist('services')
        
        print(f"DEBUG: POST данные получены: {request.POST}")
        
        if client_name and phone and master_id and appointment_date and appointment_time:
            try:
                # Создаем новый заказ
                master = Master.objects.get(id=master_id)
                
                # Объединяем дату и время
                datetime_str = f"{appointment_date} {appointment_time}"
                appointment_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                
                # Создаем заказ с правильными полями
                order = Order.objects.create(
                    client_name=client_name,
                    phone=phone,
                    master=master,
                    appointment_date=appointment_datetime,
                    status='not_approved',
                    comment=comment,
                    date_created=timezone.now()
                )
                
                print(f"DEBUG: Заказ создан с ID: {order.id}")
                messages.success(request, f'Заявка принята! Номер заявки: #{order.id}')
                return redirect('core:thanks')
                
            except Exception as e:
                print(f"DEBUG: Ошибка: {str(e)}")
                messages.error(request, f'Ошибка при создании заявки: {str(e)}')
        else:
            print(f"DEBUG: Не все поля заполнены")
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
    
    # Получаем данные для формы
    active_masters = Master.objects.filter(is_active=True)
    all_services = Service.objects.all()
    popular_services = Service.objects.filter(is_popular=True)[:3] if hasattr(Service, 'is_popular') else []
    recent_reviews = Review.objects.filter(is_published=True)[:3] if hasattr(Review, 'is_published') else []
    
    context = {
        'masters': active_masters,
        'services': all_services,
        'popular_services': popular_services,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'landing.html', context)

def booking(request):
    """Страница записи"""
    if request.method == 'POST':
        # Получаем данные из формы
        client_name = request.POST.get('client_name')
        phone = request.POST.get('phone')
        master_id = request.POST.get('master')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        comment = request.POST.get('comment')
        services = request.POST.getlist('services')
        
        if client_name and phone and master_id and appointment_date and appointment_time:
            try:
                # Создаем новый заказ
                master = Master.objects.get(id=master_id)
                
                # Объединяем дату и время
                datetime_str = f"{appointment_date} {appointment_time}"
                appointment_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                
                # Создаем заказ
                order = Order.objects.create(
                    client_name=client_name,
                    phone=phone,
                    master=master,
                    appointment_date=appointment_datetime,
                    status='not_approved',
                    comment=comment,
                    date_created=timezone.now()
                )
                
                messages.success(request, f'Заявка принята! Номер заявки: #{order.id}')
                return redirect('core:thanks')
                
            except Exception as e:
                messages.error(request, f'Ошибка при создании заявки: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
    
    context = {
        'masters': Master.objects.all(),
        'services': Service.objects.all(),
    }
    return render(request, 'core/booking.html', context)

def orders_list(request):
    """Список заявок"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Персонал видит все заявки
            orders = Order.objects.all().order_by('-date_created')
        else:
            # Обычные пользователи видят только свои заявки (по имени)
            orders = Order.objects.filter(client_name=request.user.username).order_by('-date_created')
    else:
        # Неавторизованные пользователи перенаправляются на вход
        return redirect('users:login')
    
    context = {
        'orders': orders,
        'masters': Master.objects.all(),
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    """Детали заявки"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Проверяем права доступа
        if not request.user.is_staff and order.client_name != request.user.username:
            # Обычный пользователь пытается посмотреть чужую заявку
            messages.error(request, 'У вас нет прав для просмотра этой заявки')
            return redirect('core:orders_list')
        
        master = Master.objects.get(id=order.master_id) if hasattr(order, 'master_id') else None
        services = Service.objects.all()
    except Order.DoesNotExist:
        raise Http404("Заявка не найдена")

    context = {
        'order': order,
        'master': master,
        'services': services,
    }
    return render(request, 'core/order_detail.html', context)

def services(request):
    """Страница услуг"""
    all_services = Service.objects.all()
    popular_services = Service.objects.filter(is_popular=True) if hasattr(Service, 'is_popular') else []
    
    context = {
        'all_services': all_services,
        'popular_services': popular_services,
    }
    return render(request, 'core/services.html', context)

def masters(request):
    """Страница мастеров"""
    active_masters = Master.objects.filter(is_active=True).prefetch_related('services') if hasattr(Master, 'is_active') else Master.objects.all()
    
    context = {
        'masters': active_masters,
    }
    return render(request, 'core/masters.html', context)

def master_detail(request, master_id):
    """Детальная страница мастера"""
    master = get_object_or_404(Master, id=master_id, is_active=True) if hasattr(Master, 'is_active') else get_object_or_404(Master, id=master_id)
    master_reviews = Review.objects.filter(master=master, is_published=True) if hasattr(Review, 'is_published') else []
    
    context = {
        'master': master,
        'reviews': master_reviews,
    }
    return render(request, 'core/master_detail.html', context)

def reviews(request):
    """Страница отзывов"""
    published_reviews = Review.objects.filter(is_published=True).select_related('master') if hasattr(Review, 'is_published') else []
    
    context = {
        'reviews': published_reviews,
    }
    return render(request, 'core/reviews.html', context)

def thanks(request):
    """Страница благодарности за заявку"""
    return render(request, 'core/thanks.html')