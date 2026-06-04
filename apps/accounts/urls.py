from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("signup/", SignupUser.as_view(), name="signup"),
    path("logout/", LogoutUser.as_view(), name="logout"),
]
