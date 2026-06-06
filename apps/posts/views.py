from django.shortcuts import render
from .models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from apps.profiles.models import Follow


# ---------------- POST LIST ----------------
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Post
from apps.profiles.models import Follow

class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        # چون author خودش به Profile وصل است، فقط خود author را select_related می‌کنیم
        # و دیتای مدل User متصل به آن را هم با 'author__user' می‌آوریم
        return Post.objects.select_related('author', 'author__user').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context["follow_set"] = set(
                Follow.objects.filter(
                    follower=self.request.user.profile
                ).values_list("following_id", flat=True)
            )
        else:
            context["follow_set"] = set()

        return context
# ---------------- POST CREATE ----------------
class PostCreate(CreateView):
    model = Post
    fields = ["content", "image"]
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("posts:postlist")

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# ---------------- POST DETAIL ----------------
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"


# ---------------- POST DELETE ----------------
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:postlist")
    template_name = "posts/post_delete.html"


# ---------------- POST UPDATE ----------------
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["image", "content"]
    context_object_name = "post"
    success_url = reverse_lazy("posts:postlist")
    template_name = "posts/post_update.html"

    def form_valid(self, form):
        form.instance.is_edited = True
        return super().form_valid(form)