from django.urls import path
from .views import *
app_name = 'profiles'

urlpatterns = [
    # path("<str>:username>/", profile_view, name="profile")
    path("my_profile/", MyProfileView.as_view(), name="my_profile"),
    path("<str:username>/", ProfileDetailView.as_view(), name="profile"),
        path("follow/<int:profile_id>/", follow_user),
    path("unfollow/<int:profile_id>/", unfollow_user),
]
