from apps.accounts.models import Profile
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    content  = models.TextField(null=True)
    is_edited = models.BooleanField(default=False)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    likes = models.ManyToManyField(Profile, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.content[:50]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]

