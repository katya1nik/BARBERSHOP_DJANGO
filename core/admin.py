from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from .models import Master, Service, Order, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    fields = ('client_name', 'text', 'rating', 'is_published', 'ai_checked_status')
    readonly_fields = ('ai_checked_status',)
    can_delete = True


class ServiceInline(admin.TabularInline):
    """Инлайн для услуг на странице мастера"""
    model = Master.services.through
    extra = 0
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги мастера"


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'specialization', 'is_active', 'services_count')
    list_filter = ('is_active', 'experience', 'specialization')
    search_fields = ('name', 'phone', 'specialization')
    list_editable = ('is_active',)
    inlines = [ReviewInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'phone', 'photo')
        }),
        ('Профессиональная информация', {
            'fields': ('specialization', 'experience', 'address')
        }),
        ('Услуги и статус', {
            'fields': ('services', 'is_active')
        }),
    )
    filter_horizontal = ('services',)

    def services_count(self, obj):
        """Количество услуг мастера"""
        return obj.services.count()
    services_count.short_description = 'Количество услуг'

    actions = ['activate_masters', 'deactivate_masters']

    def activate_masters(self, request, queryset):
        """Активировать выбранных мастеров"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} мастеров.')
    activate_masters.short_description = 'Активировать выбранных мастеров'

    def deactivate_masters(self, request, queryset):
        """Деактивировать выбранных мастеров"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} мастеров.')
    deactivate_masters.short_description = 'Деактивировать выбранных мастеров'


class PopularServiceFilter(admin.SimpleListFilter):
    """Кастомный фильтр для популярных услуг"""
    title = 'популярность'
    parameter_name = 'popularity'

    def lookups(self, request, model_admin):
        return (
            ('popular', 'Популярные'),
            ('not_popular', 'Не популярные'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'popular':
            return queryset.filter(is_popular=True)
        if self.value() == 'not_popular':
            return queryset.filter(is_popular=False)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular', 'masters_count')
    list_filter = (PopularServiceFilter, 'price')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_popular')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image')
        }),
        ('Коммерческая информация', {
            'fields': ('price', 'duration', 'is_popular')
        }),
    )

    def masters_count(self, obj):
        """Количество мастеров, предоставляющих услугу"""
        return obj.masters.count()
    masters_count.short_description = 'Количество мастеров'

    actions = ['make_popular', 'make_not_popular']

    def make_popular(self, request, queryset):
        """Сделать услуги популярными"""
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'Отмечено как популярные: {updated} услуг.')
    make_popular.short_description = 'Отметить как популярные'

    def make_not_popular(self, request, queryset):
        """Убрать популярность услуг"""
        updated = queryset.update(is_popular=False)
        self.message_user(request, f'Убрана популярность у {updated} услуг.')
    make_not_popular.short_description = 'Убрать популярность'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'master', 'status')
    list_filter = ('status', 'master')
    search_fields = ('client_name', 'phone')
    list_editable = ('status',)
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('client_name', 'phone')
        }),
        ('Детали заказа', {
            'fields': ('master', 'services')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
    )
    filter_horizontal = ('services',)

    actions = ['approve_orders', 'cancel_orders', 'complete_orders']

    def approve_orders(self, request, queryset):
        """Подтвердить заказы"""
        updated = queryset.update(status='approved')
        self.message_user(request, f'Подтверждено {updated} заказов.')
    approve_orders.short_description = 'Подтвердить заказы'

    def cancel_orders(self, request, queryset):
        """Отменить заказы"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'Отменено {updated} заказов.')
    cancel_orders.short_description = 'Отменить заказы'

    def complete_orders(self, request, queryset):
        """Завершить заказы"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'Завершено {updated} заказов.')
    complete_orders.short_description = 'Завершить заказы'


class AIStatusFilter(admin.SimpleListFilter):
    """Кастомный фильтр для статуса проверки ИИ"""
    title = 'статус проверки ИИ'
    parameter_name = 'ai_status'

    def lookups(self, request, model_admin):
        return (
            ('checked', 'Проверено'),
            ('cancelled', 'Отменено'),
            ('in_progress', 'В процессе'),
            ('not_checked', 'Не проверено'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'checked':
            return queryset.filter(ai_checked_status='ai_checked_true')
        if self.value() == 'cancelled':
            return queryset.filter(ai_checked_status='ai_cancelled')
        if self.value() == 'in_progress':
            return queryset.filter(ai_checked_status='ai_checked_in_progress')
        if self.value() == 'not_checked':
            return queryset.filter(ai_checked_status='ai_checked_false')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'text_preview', 'is_published', 'ai_status_display', 'created_at')
    list_display_links = ('client_name', 'text_preview')
    list_filter = ('rating', 'is_published', AIStatusFilter, 'created_at', 'master')
    search_fields = ('client_name', 'text', 'master__name')
    list_editable = ('is_published',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Информация об отзыве', {
            'fields': ('client_name', 'master', 'rating', 'text', 'photo')
        }),
        ('Статус публикации', {
            'fields': ('is_published', 'ai_checked_status', 'created_at')
        }),
    )

    def text_preview(self, obj):
        """Предварительный просмотр текста отзыва"""
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text
    text_preview.short_description = 'Текст отзыва'

    def ai_status_display(self, obj):
        """Красивое отображение статуса ИИ"""
        status_colors = {
            'ai_checked_true': 'green',
            'ai_cancelled': 'red',
            'ai_checked_in_progress': 'orange',
            'ai_checked_false': 'gray',
        }
        color = status_colors.get(obj.ai_checked_status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_ai_checked_status_display()
        )
    ai_status_display.short_description = 'Статус ИИ'

    actions = ['publish_reviews', 'unpublish_reviews']

    def publish_reviews(self, request, queryset):
        """Опубликовать отзывы"""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Опубликовано {updated} отзывов.')
    publish_reviews.short_description = 'Опубликовать отзывы'

    def unpublish_reviews(self, request, queryset):
        """Снять с публикации отзывы"""
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Снято с публикации {updated} отзывов.')
    unpublish_reviews.short_description = 'Снять с публикации'
