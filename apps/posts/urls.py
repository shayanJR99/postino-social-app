from django.urls import path
from .views import PostDelete,PostUpdate,PostList,PostCreate,PostDetail,unlike_post,like_post,PostCommentView

app_name = 'posts'

urlpatterns = [
    path("", PostList.as_view(), name="postlist"),
    path("create/", PostCreate.as_view(), name="postcreate"),
    path("<int:pk>/", PostDetail.as_view(), name="detail"),
    path("<int:pk>/update/", PostUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="delete"),
    path("like/<int:post_id>/", like_post, name="like"),
    path("unlike/<int:post_id>/", unlike_post, name="unlike"),
    path(
        "post/<int:post_id>/comments/",
        PostCommentView.as_view(),
        name="post_comments",),
]

