from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import User
from .forms import SignupForm
from django.contrib.auth.views import LogoutView
# Create your views here.


# accounts/views.py

from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView


class LoginUser(LoginView):

    template_name = "accounts/login.html"

    redirect_authenticated_user = True          
    
    
class LogoutUser(LogoutView):

    next_page = "accounts:login"

    
class SignupUser(CreateView):

    model = User

    form_class = SignupForm

    template_name = "accounts/signup.html"

    success_url = reverse_lazy(
        "accounts:login"
    )