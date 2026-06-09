from django.urls import path
from .views import *

app_name = "profiles"

urlpatterns = [
    # ۱. ابتدا آدرس‌های ثابت و مشخص (Static)
    path("my_profile/", MyProfileView.as_view(), name="my_profile"),
    path("my_profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"), # <- این خط را به ردیف دوم بیاورید
    path("toggle-follow/<int:profile_id>/", toggle_follow, name="toggle_follow"),
    
    # ۲. سپس آدرس‌های متغیر و داینامیک (Dynamic)
    path("<str:username>/", ProfileDetailView.as_view(), name="profile"),
    path("<str:username>/<str:relation_type>/", user_relations_list, name="user_relations"),
]