from django.db import models
from django.db.models import F, Q

from apps.accounts.models import Profile


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="following_relations"
    )

    following = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="follower_relations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow"
            ),
            models.CheckConstraint(
                condition=~Q(follower=F("following")),
                name="prevent_self_follow"
            ),
        ]

        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
        ]

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"