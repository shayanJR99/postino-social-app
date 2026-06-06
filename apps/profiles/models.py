from django.db import models
from apps.accounts.models import Profile
from django.core.exceptions import ValidationError

# Create your models here.

class Follow(models.Model):
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            )
        ]
    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You can't follow yourself")