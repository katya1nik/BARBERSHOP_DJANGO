from django.contrib import admin
from .models import Master, Service, Order, Review


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    """Админка для мастеров"""
    list_display = ('name', 'phone', 'experience', 'specialization', 'is_active')
    list_filter = ('is_active', 'experience')
    search_fields = ('name', 'phone', 'specialization')
    filter_horizontal = ('services',)
    list_editable = ('is_active',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка для услуг"""
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)
    list_editable = ('is_popular',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка для заказов"""
    list_display = ('client_name', 'phone', 'master', 'status', 'appointment_date', 'date_created')
    list_filter = ('status', 'date_created', 'master')
    search_fields = ('client_name', 'phone')
    filter_horizontal = ('services',)
    date_hierarchy = 'appointment_date'
    list_editable = ('status',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов"""
    list_display = ('client_name', 'master', 'rating', 'is_published', 'created_at')
    list_filter = ('rating', 'is_published', 'master')
    search_fields = ('client_name', 'text')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
