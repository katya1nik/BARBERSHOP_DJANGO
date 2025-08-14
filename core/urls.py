from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('services/', views.services, name='services'),
    path('masters/', views.masters, name='masters'),
    path('reviews/', views.reviews, name='reviews'),
    path('booking/', views.booking, name='booking'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders_list, name='orders_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]