from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.accounts.models import Profile
from .models import Follow

# ---------------- تابع کمکی بهینه‌شده ----------------
def get_profile_social_data(profile):
    posts = profile.posts.all()

    # دریافت لیست واقعی پروفایل‌ها با استفاده از values_list یا select_related
    followers_profiles = Profile.objects.filter(following_relations__following=profile)
    following_profiles = Profile.objects.filter(follower_relations__follower=profile)

    return {
        "posts": posts,
        "posts_count": posts.count(),
        "followers": followers_profiles,           # لیست پروفایل‌های فالوورها
        "following": following_profiles,           # لیست پروفایل‌های فالویینگ‌ها
        "followers_count": followers_profiles.count(),
        "following_count": following_profiles.count(),
    }


# ---------------- مشخصات پروفایل دیگران ----------------
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/view_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        
        # تزریق اطلاعات آمار و لیست‌ها
        context.update(get_profile_social_data(profile))

        # بررسی وضعیت فالو بودن برای کاربر لاگین شده
        if self.request.user.is_authenticated:
            context["is_following"] = Follow.objects.filter(
                follower=self.request.user.profile,
                following=profile
            ).exists()
        else:
            context["is_following"] = False

        return context


# ---------------- پروفایل من ----------------
class MyProfileView(DetailView):
    model = Profile
    template_name = "profiles/my_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context.update(get_profile_social_data(profile))
        return context


# ---------------- ویو یکپارچه فالو / آنفالو (Toggle) ----------------
@login_required
@require_POST  # امنیت بیشتر: این ویو فقط درخواست‌های POST را می‌پذیرد
def toggle_follow(request, profile_id):
    target_profile = get_object_or_404(Profile, id=profile_id)
    user_profile = request.user.profile

    # کاربر نباید بتواند خودش را فالو کند
    if user_profile != target_profile:
        follow_record = Follow.objects.filter(follower=user_profile, following=target_profile)
        
        if follow_record.exists():
            # اگر از قبل فالو بود، آنفالو کن
            follow_record.delete()
        else:
            # اگر فالو نبود، فالو کن
            Follow.objects.create(follower=user_profile, following=target_profile)

    # بازگشت به صفحه‌ای که کاربر در آن قرار داشت
    return redirect(request.META.get("HTTP_REFERER", "/"))