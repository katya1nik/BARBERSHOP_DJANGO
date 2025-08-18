from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('test/', views.test_page, name='test'),
    path('test-reviews/', views.test_reviews, name='test_reviews'),
    path('services/', views.services, name='services'),
    path('masters/', views.masters, name='masters'),
    path('masters/<int:master_id>/', views.master_detail, name='master_detail'),
    path('reviews/', views.display_reviews, name='reviews'),
    path('booking/', views.booking, name='booking'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]