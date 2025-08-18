from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Master, Review, Order, Service
# from .forms import ReviewForm, OrderForm

import datetime


# ========== КЛАССОВЫЕ ПРЕДСТАВЛЕНИЯ (CBV) ==========

class LandingView(TemplateView):
    """Главная страница (landing) с блоками мастеров и отзывов"""
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем активных мастеров, сортируем по убыванию ID
        context['masters'] = (
            Master.objects.filter(is_active=True).order_by('-id')[:6]
        )
        # Получаем опубликованные отзывы
        context['reviews'] = (
            Review.objects
            .filter(is_published=True)
            .select_related('master')[:6]
        )
        # Получаем популярные услуги
        context['popular_services'] = (
            Service.objects.filter(is_popular=True)[:4]
        )
        return context


class ThanksView(TemplateView):
    """Страница благодарности"""
    template_name = 'core/thanks.html'


class OrdersListView(LoginRequiredMixin, ListView):
    """Список всех заявок с поиском через Q-объекты"""
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Простой queryset без сложных связей
        # Суперпользователи видят все заявки, обычные пользователи - только свои
        if self.request.user.is_superuser:
            queryset = super().get_queryset().prefetch_related('services')
        else:
            queryset = super().get_queryset().filter(client_name=self.request.user.username).prefetch_related('services')

        # Получаем параметры поиска
        search_query = self.request.GET.get('search', '').strip()
        search_by_name = self.request.GET.get('search_by_name')
        search_by_phone = self.request.GET.get('search_by_phone')

        # Если нет поискового запроса, возвращаем заявки
        if not search_query:
            return queryset

        # Создаем Q-объект для поиска
        search_conditions = Q()

        # Если не выбран ни один чекбокс, по умолчанию ищем по имени
        if not any([search_by_name, search_by_phone]):
            search_by_name = True

        # Добавляем условия поиска в зависимости от выбранных чекбоксов
        if search_by_name:
            search_conditions |= Q(client_name__icontains=search_query)
        if search_by_phone:
            search_conditions |= Q(phone__icontains=search_query)

        # Применяем фильтр к queryset
        return queryset.filter(search_conditions)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем параметры поиска в контекст для сохранения состояния
        context['search_query'] = self.request.GET.get('search', '')
        context['search_by_name'] = self.request.GET.get('search_by_name')
        context['search_by_phone'] = self.request.GET.get('search_by_phone')
        
        # Отладочная информация
        context['debug_user'] = str(self.request.user)
        context['debug_is_superuser'] = self.request.user.is_superuser
        context['debug_user_id'] = self.request.user.id
        
        # Тестовая переменная
        from django.utils import timezone
        context['now'] = timezone.now()
        
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Детали конкретной заявки"""
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('services')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Отладочная информация
        order = context['order']
        context['debug_services_count'] = order.services.count() if hasattr(order, 'services') else 'Нет services'
        context['debug_services_type'] = type(order.services).__name__ if hasattr(order, 'services') else 'Нет services'
        
        return context


class ReviewCreateView(CreateView):
    """Создание нового отзыва"""
    model = Review
    form_class = None
    template_name = 'core/add_review.html'
    success_url = reverse_lazy('core:thanks')

    def form_valid(self, form):
        # Автоматически публикуем отзыв
        form.instance.is_published = True
        # Добавляем success-сообщение
        messages.success(
            self.request,
            'Спасибо за ваш отзыв! Он был успешно добавлен.'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оставить отзыв'
        return context


class OrderCreateView(CreateView):
    """Создание новой заявки"""
    model = Order
    form_class = None
    template_name = 'core/book_appointment.html'
    success_url = reverse_lazy('core:thanks')

    def form_valid(self, form):
        # Устанавливаем статус "ожидает подтверждения"
        form.instance.status = 'not_approved'
        # Добавляем success-сообщение
        messages.success(
            self.request,
            'Ваша заявка успешно отправлена! '
            'Мы свяжемся с вами для подтверждения.'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записаться к мастеру'
        return context


# ========== ДОПОЛНИТЕЛЬНЫЕ ПРЕДСТАВЛЕНИЯ ==========

def master_detail(request, master_id):
    """Детальная страница мастера"""
    master = get_object_or_404(Master, id=master_id, is_active=True)
    master_reviews = Review.objects.filter(
        master=master, is_published=True
    )
    master_services = master.services.all()
    context = {
        'master': master,
        'reviews': master_reviews,
        'services': master_services,
    }
    return render(request, 'core/master_detail.html', context)


def get_master_services(request, master_id):
    """API для получения услуг конкретного мастера (для AJAX)"""
    try:
        master = Master.objects.get(id=master_id, is_active=True)
        services = master.services.all().values(
            'id', 'name', 'price', 'duration'
        )
        return JsonResponse({
            'success': True,
            'services': list(services)
        }, json_dumps_params={'ensure_ascii': False})
    except Master.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Мастер не найден'
        }, json_dumps_params={'ensure_ascii': False})


# ========== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ==========

def services(request):
    """Страница со списком услуг"""
    all_services = Service.objects.all()
    popular_services = Service.objects.filter(is_popular=True)
    
    context = {
        'all_services': all_services,
        'popular_services': popular_services,
    }
    
    return render(request, 'core/services.html', context)

def masters(request):
    """Страница со списком мастеров"""
    masters_list = (
        Master.objects
        .filter(is_active=True)
        .prefetch_related('services')
    )
    
    # Отладочная информация
    print(f"DEBUG: Найдено мастеров: {masters_list.count()}")
    for master in masters_list:
        print(f"DEBUG: Мастер {master.name} - услуг: {master.services.count()}")
    
    return render(request, 'core/masters.html', {'masters': masters_list})

def test_page(request):
    """Простая тестовая страница"""
    return render(request, 'core/test.html', {'message': 'Тест работает!'})

def test_reviews(request):
    """Тестовая функция для проверки URL маршрутизации"""
    print("DEBUG: Функция test_reviews вызвана")
    
    from django.http import HttpResponse
    return HttpResponse("""
    <html>
    <head><title>Тест test_reviews</title></head>
    <body>
        <h1>Функция test_reviews работает!</h1>
        <p>Если вы видите этот текст, значит URL маршрутизация работает.</p>
        <p>Проблема в функции reviews или в шаблоне.</p>
    </body>
    </html>
    """)

def display_reviews(request):
    """Страница с отзывами - новая функция"""
    print("DEBUG: Функция display_reviews вызвана")
    
    try:
        # Импортируем модель Review
        from .models import Review
        
        # Получаем все отзывы
        reviews_list = Review.objects.all()
        count = reviews_list.count()
        
        print(f"DEBUG: Отзывов найдено: {count}")
        
        # Создаем контекст с реальными отзывами
        context = {
            'reviews': reviews_list,
        }
        
        print("DEBUG: Контекст создан, пытаюсь рендерить новый файл")
        response = render(request, 'core/final_reviews.html', context)
        print("DEBUG: Новый файл успешно отрендерен")
        
        return response
        
    except Exception as e:
        print(f"DEBUG: Ошибка при рендеринге нового файла: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Возвращаем ошибку
        from django.http import HttpResponse
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>Ошибка нового файла</title></head>
        <body>
            <h1>Ошибка при загрузке нового файла</h1>
            <p>Ошибка: {str(e)}</p>
            <p>Проверьте консоль сервера для деталей.</p>
        </body>
        </html>
        """)

def booking(request):
    """Страница записи к мастеру"""
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            client_name = request.POST.get('client_name')
            phone = request.POST.get('phone')
            master_id = request.POST.get('master')
            services_ids = request.POST.getlist('services')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            comment = request.POST.get('comment', '')
            
            print(f"DEBUG: Получены данные: client_name={client_name}, phone={phone}, master_id={master_id}, services_ids={services_ids}")
            
            # Проверяем обязательные поля
            if not all([client_name, phone, master_id, services_ids]):
                missing_fields = []
                if not client_name: missing_fields.append('имя')
                if not phone: missing_fields.append('телефон')
                if not master_id: missing_fields.append('мастер')
                if not services_ids: missing_fields.append('услуги')
                
                return JsonResponse({
                    'success': False,
                    'message': f'Пожалуйста, заполните все обязательные поля: {", ".join(missing_fields)}'
                }, json_dumps_params={'ensure_ascii': False})
            
            # Создаем заказ с существующей структурой
            from django.db import connection
            
            with connection.cursor() as cursor:
                # Сначала проверим структуру таблицы
                cursor.execute("PRAGMA table_info(core_order)")
                columns = cursor.fetchall()
                print(f"DEBUG: Структура таблицы core_order:")
                for col in columns:
                    print(f"  {col[1]} ({col[2]})")
                
                # Получаем названия полей
                column_names = [col[1] for col in columns]
                print(f"DEBUG: Названия полей: {column_names}")
                
                # Создаем заказ, используя только существующие поля
                if 'service' in column_names:
                    # Если есть поле service
                    cursor.execute("""
                        INSERT INTO core_order (client_name, phone, master_id, service, status, created_at)
                        VALUES (%s, %s, %s, %s, %s, datetime('now'))
                    """, [client_name, phone, master_id, services_ids[0], 'not_approved'])
                else:
                    # Если поля service нет, вставляем только основные поля
                    cursor.execute("""
                        INSERT INTO core_order (client_name, phone, master_id, status, created_at)
                        VALUES (%s, %s, %s, %s, datetime('now'))
                    """, [client_name, phone, master_id, 'not_approved'])
                
                order_id = cursor.lastrowid
                
                # Добавляем все услуги в связующую таблицу
                for service_id in services_ids:
                    cursor.execute("""
                        INSERT INTO core_order_services (order_id, service_id)
                        VALUES (%s, %s)
                    """, [order_id, service_id])
            
            print(f"DEBUG: Заказ создан успешно: ID={order_id}")
            
            return JsonResponse({
                'success': True,
                'message': 'Заявка успешно создана! Мы свяжемся с вами для подтверждения.'
            }, json_dumps_params={'ensure_ascii': False})
            
        except Exception as e:
            print(f"DEBUG: Ошибка при создании заказа: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return JsonResponse({
                'success': False,
                'message': f'Ошибка при создании заявки: {str(e)}'
            }, json_dumps_params={'ensure_ascii': False})
    
    # GET запрос - показываем форму
    masters_list = Master.objects.filter(is_active=True)
    services_list = Service.objects.all()  # Все услуги, а не только популярные
    
    context = {
        'masters': masters_list,
        'services': services_list,  # Передаем services вместо popular_services
    }
    
    return render(request, 'core/booking.html', context)

# ========== СТАРЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ СОВМЕСТИМОСТИ ==========

def home(request):
    """Редирект на новую главную страницу"""
    return redirect('core:landing')


def add_review(request):
    """Редирект на новую страницу создания отзыва"""
    return redirect('core:create_review')


def book_appointment(request):
    """Редирект на новую страницу создания заявки"""
    return redirect('core:create_order')
