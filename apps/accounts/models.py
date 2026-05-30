from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """مدیریت ساخت کاربران برای مدل سفارشی"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not None and extra_fields.get("is_staff") is False:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not None and extra_fields.get("is_superuser") is False:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # معمولاً در شروع True می‌گذارند مگر اینکه تایید ایمیل داشته باشید
    is_verified = models.BooleanField(default=False) # برای تایید ایمیل یا شماره موبایل

    # تنظیمات مربوط به فیلد شناسایی
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] # فیلدهایی که موقع createsuperuser پرسیده می‌شوند

    # زمان‌بندی‌ها
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager() # متصل کردن مدیر به مدل

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    first_name = models.CharField(max_length=255,blank=True)

    last_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="profiles/",blank=True,null=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)