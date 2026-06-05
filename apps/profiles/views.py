from django.shortcuts import render
from apps.accounts.models import Profile
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404    
# Create your views here.

# FBV profile view
def profile_view(request, username):
    u = Profile.objects.get_object_or_404(username=username)
    p = Profile.objects.get(user=u)
    return render(request, 'profiles/profile.html', {'profile': p})
# CBV profile view
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/view_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Profile,
            username=self.kwargs['username']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["posts"] = self.object.posts.all()
        context["posts_count"] = self.object.posts.count()

        return context
    
    
class MyProfileView(DetailView):
    model = Profile
    template_name = 'profiles/my_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.object

        posts = profile.posts.all()   # چون related_name="posts"

        context["posts"] = posts
        context["posts_count"] = posts.count()

        return context