from django.urls import path
from .views import PostDelete,PostUpdate,PostList,PostCreate,PostDetail

app_name = 'posts'

urlpatterns = [
    path("", PostList.as_view(), name="postlist"),
    path("create/", PostCreate.as_view(), name="postcreate"),
    path("<int:pk>/", PostDetail.as_view(), name="detail"),
    path("<int:pk>/update/", PostUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="delete"),
]

