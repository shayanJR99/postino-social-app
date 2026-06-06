from django.shortcuts import render
from apps.accounts.models import Profile
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
# Create your views here.


# FBV profile view
def profile_view(request, username):
    u = Profile.objects.get_object_or_404(username=username)
    p = Profile.objects.get(user=u)
    return render(request, "profiles/profile.html", {"profile": p})


# CBV profile view
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/view_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.object

        context["posts"] = profile.posts.all()
        context["posts_count"] = profile.posts.count()

        context["followers"] = Follow.objects.filter(following=profile)
        context["following"] = Follow.objects.filter(follower=profile)

        context["followers_count"] = context["followers"].count()
        context["following_count"] = context["following"].count()

        return context


class MyProfileView(DetailView):
    model = Profile
    template_name = "profiles/my_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.object

        posts = profile.posts.all()  # چون related_name="posts"

        context["posts"] = posts
        context["posts_count"] = posts.count()

        return context


# --------------------------------------------------------------------------------------
from .models import Follow
from apps.profiles.models import Profile
from django.http import JsonResponse
# follow


def follow_user(request, profile_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    target = Profile.objects.get(id=profile_id)

    if request.user.profile == target:
        return JsonResponse({"error": "can't follow yourself"}, status=400)

    obj, created = Follow.objects.get_or_create(
        follower=request.user.profile, following=target
    )

    return JsonResponse({"followed": created})


def unfollow_user(request, profile_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    target = Profile.objects.get(id=profile_id)

    Follow.objects.filter(follower=request.user.profile, following=target).delete()

    return JsonResponse({"unfollowed": True})
