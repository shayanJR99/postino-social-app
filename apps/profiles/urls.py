from django.urls import path
from .views import MyProfileView, ProfileDetailView, toggle_follow

app_name = "profiles"

urlpatterns = [
    path("my_profile/", MyProfileView.as_view(), name="my_profile"),
    path("<str:username>/", ProfileDetailView.as_view(), name="profile"),
    
    # آدرس جدید سیستم یکپارچه توگل فالو با شناسه پروفایل
    path("toggle-follow/<int:profile_id>/", toggle_follow, name="toggle_follow"),
]