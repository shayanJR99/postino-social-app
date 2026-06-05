from django.shortcuts import render
from .models import Post
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView,CreateView


# Create your views here.


class PostList(LoginRequiredMixin,ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"
    paginate_by = 5


    
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
    
    
class PostDetail(LoginRequiredMixin,DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:postlist")
    template_name = "posts/post_delete.html"
    
    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        "image",
        "content",
    ]
    context_object_name = "post"
    success_url = reverse_lazy("posts:postlist")
    template_name = "posts/post_update.html"
    
    
    def form_valid(self, form):
        form.instance.is_edited = True
        return super().form_valid(form)