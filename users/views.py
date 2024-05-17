from typing import Any
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
import maindj.settings

from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

class LoginUser(LoginView): 
  form_class = AuthenticationForm
  template_name = 'users/login.html'
  extra_context = {'title': 'Авторизация'} 


class RegisterUser(CreateView):
  form_class = RegisterUserForm
  template_name = 'users/register.html'
  extra_context = {'title': "Регистрация"}
  success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
  model = get_user_model()
  form_class = ProfileUserForm
  template_name = 'users/profile.html'
  extra_context = {
    'title': "Профиль пользователя",
    'default_image': maindj.settings.DEFAULT_USER_IMAGE,
    }
 
  def get_success_url(self):
    return reverse_lazy('users:profile')
  
  def get_object(self, queryset=None):
    return self.request.user
  
  
class UserPasswordChange(PasswordChangeView): 
  form_class = UserPasswordChangeForm
  success_url = reverse_lazy("users:password_change_done")
  template_name = 'users/password_change_form.html'
  extra_context = {'title': "Сменить пароль"}
