from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from apps.accounts.models import Profile

class Follow(models.Model):
    # کسی که فالو می‌کند
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='following_relations'
    )
    # کسی که فالو می‌شود
    following = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follower_relations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # جلوگیری از فالو تکراری
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            ),
            # اصلاح این بخش: تغییر check به condition
            models.CheckConstraint(
                condition=~models.Q(follower=models.F('following')), # اینجا کلمه condition جایگزین شد
                name='prevent_self_follow'
            )
        ]