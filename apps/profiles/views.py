from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import models  # <-- ۱. اضافه شدن این خط برای حل مشکل سرچ و models.Q

from apps.accounts.models import Profile
from apps.posts.models import Post # <-- اضافه شدن مدل پست جهت فیلتر دقیق‌تر
from .models import Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import ProfileUpdateForm

# ---------------- تابع کمکی بهینه‌شده ----------------
def get_profile_social_data(profile):
    # اصلاح جزئی برای واکشی دقیق پست‌های این پروفایل بدون اتکا به related_name
    posts = Post.objects.filter(author=profile)

    # دریافت لیست واقعی پروفایل‌ها با استفاده از روابط مدل Follow
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

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "profiles/edit-profile.html"
    success_url = reverse_lazy("profiles:my_profile")

    def get_object(self, queryset=None):
        # تلاش برای گرفتن پروفایل کاربر؛ اگر نبود، خودکار ساخته می‌شود (get_or_create)
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

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


# ---------------- لیست فالوورها و فالویینگ‌ها همراه با سرچ ----------------
def user_relations_list(request, username, relation_type):
    target_profile = get_object_or_404(Profile, username=username)
    
    # گرفتن عبارت جستجو شده از آدرس URL
    search_query = request.GET.get('search', '')

    if relation_type == 'followers':
        profiles = Profile.objects.filter(following_relations__following=target_profile).select_related('user')
        template_name = 'profiles/follower.html'
    elif relation_type == 'following':
        profiles = Profile.objects.filter(follower_relations__follower=target_profile).select_related('user')
        template_name = 'profiles/following.html'
    else:
        return redirect('profiles:profile', username=username)

    # اعمال فیلتر جستجو (بدون ارور به خاطر اضافه شدن خط ۴)
    if search_query:
        profiles = profiles.filter(
            models.Q(username__icontains=search_query) | 
            models.Q(first_name__icontains=search_query)
        )

    # مجموعه آیدی کسانی که کاربر در حال حاضر آن‌ها را فالو دارد
    follow_set = set()
    if request.user.is_authenticated:
        follow_set = set(
            Follow.objects.filter(
                follower=request.user.profile
            ).values_list("following_id", flat=True)
        )

    context = {
        'target_profile': target_profile,
        'profiles_list': profiles,
        'follow_set': follow_set,
        'search_query': search_query,
    }
    return render(request, template_name, context)