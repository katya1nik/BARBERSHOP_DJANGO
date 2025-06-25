from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Master, Service, Order, Review


def is_staff_user(user):
    return user.is_staff


def landing(request):
    """Главная страница с формой записи"""
    if request.method == 'POST':
        # Получаем данные из формы
        client_name = request.POST.get('name')
        phone = request.POST.get('phone')
        master_id = request.POST.get('master')
        service_ids = request.POST.getlist('services')
        appointment_date = request.POST.get('appointment_date')
        comment = request.POST.get('comment', '')
               
        try:
            # Получаем мастера
            master = Master.objects.get(id=int(master_id)) if master_id else Master.objects.filter(is_active=True).first()
            
            # Создаем заказ
            order = Order.objects.create(
                client_name=client_name or 'Не указано',
                phone=phone or 'Не указано',
                master=master,
                appointment_date=appointment_date,
                comment=comment,
                status='not_approved'
            )
            
            # Добавляем услуги к заказу
            if service_ids:
                services = Service.objects.filter(id__in=service_ids)
                order.services.set(services)
                       
            return redirect('core:thanks')
                   
        except Exception as e:
            print(f"Ошибка создания заказа: {e}")
    
    # Получаем данные для формы
    active_masters = Master.objects.filter(is_active=True)
    all_services = Service.objects.all()
    popular_services = Service.objects.filter(is_popular=True)[:3]
    recent_reviews = Review.objects.filter(is_published=True)[:3]
    
    context = {
        'masters': active_masters,
        'services': all_services,
        'popular_services': popular_services,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'landing.html', context)


def services(request):
    """Страница услуг"""
    all_services = Service.objects.all()
    popular_services = Service.objects.filter(is_popular=True)
    
    context = {
        'all_services': all_services,
        'popular_services': popular_services,
    }
    return render(request, 'core/services.html', context)


def masters(request):
    """Страница мастеров"""
    active_masters = Master.objects.filter(is_active=True).prefetch_related('services')
    
    context = {
        'masters': active_masters,
    }
    return render(request, 'core/masters.html', context)


def master_detail(request, master_id):
    """Детальная страница мастера"""
    master = get_object_or_404(Master, id=master_id, is_active=True)
    master_reviews = Review.objects.filter(master=master, is_published=True)
    
    context = {
        'master': master,
        'reviews': master_reviews,
    }
    return render(request, 'core/master_detail.html', context)


def reviews(request):
    """Страница отзывов"""
    published_reviews = Review.objects.filter(is_published=True).select_related('master')
    
    context = {
        'reviews': published_reviews,
    }
    return render(request, 'core/reviews.html', context)


def booking(request):
    """Страница записи на прием"""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Заявка принята!'})
    
    active_masters = Master.objects.filter(is_active=True)
    all_services = Service.objects.all()
    
    context = {
        'masters': active_masters,
        'services': all_services,
    }
    return render(request, 'core/booking.html', context)


def thanks(request):
    """Страница благодарности"""
    return render(request, 'core/thanks.html')


@user_passes_test(is_staff_user)
def orders_list(request):
    """Список всех заявок (только для персонала)"""
    orders = Order.objects.all().select_related('master').prefetch_related('services').order_by('-date_created')
    
    context = {
        'orders': orders,
    }
    return render(request, 'core/orders_list.html', context)


@user_passes_test(is_staff_user)
def order_detail(request, order_id):
    """Детали конкретной заявки (только для персонала)"""
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
    }
    return render(request, 'core/order_detail.html', context)
