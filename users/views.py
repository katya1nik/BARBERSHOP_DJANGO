from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import (
    UserLoginForm, UserRegisterForm, UserProfileUpdateForm,
    UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
)
from .models import UserProfile

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Убеждаемся, что у пользователя есть профиль
        try:
            profile = self.request.user.profile
        except User.profile.RelatedObjectDoesNotExist:
            # Если профиля нет, создаем его
            UserProfile.objects.get_or_create(user=self.request.user)
        
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return response

class UserLogoutView(LogoutView):
    next_page = '/'
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            # Для GET-запросов перенаправляем на главную страницу
            return redirect(self.next_page)
        # Для POST-запросов выполняем выход
        messages.success(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)

class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Аккаунт для {username} был создан! Теперь вы можете войти в систему.')
        return response

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        # Получаем или создаем профиль пользователя
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'users/profile_update_form.html'
    form_class = UserProfileUpdateForm
    
    def get_object(self):
        # Получаем или создаем профиль пользователя
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_success_url(self):
        return reverse_lazy('users:profile_detail')
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    
    def get_success_url(self):
        return reverse_lazy('users:profile_detail')
    
    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    form_class = CustomPasswordResetForm
    
    def get_success_url(self):
        return reverse_lazy('users:password_reset_done')
    
    def form_valid(self, form):
        messages.success(self.request, 'Инструкции по восстановлению пароля отправлены на ваш email.')
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    
    def get_success_url(self):
        return reverse_lazy('users:password_reset_complete')
    
    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен! Теперь вы можете войти с новым паролем.')
        return super().form_valid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'