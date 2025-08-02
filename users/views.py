from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_field_name = 'next'
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = '/'
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Аккаунт для {username} был создан! Теперь вы можете войти в систему.')
        return response