from django import forms
from .models import Review, Order

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'master', 'services', 'appointment_date']
