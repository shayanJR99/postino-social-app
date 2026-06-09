from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from apps.profiles.models import Follow
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from .forms import CommentForm
from .models import Comment, Post
from django.urls import reverse


# ---------------- POST LIST ----------------
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
        context["follow_set"] = set(Follow.objects.filter(
                follower=self.request.user.profile
                ).values_list("following_id", flat=True))
        
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
    
    
    
# ---------------- POST like ----------------
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.likes.add(request.user.profile)

    return redirect(request.META.get("HTTP_REFERER", "/"))


# ---------------- POST unlike ----------------
@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post.likes.remove(request.user.profile)

    return redirect(request.META.get("HTTP_REFERER", "/"))




class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment.html"  # نام قالب HTML شما

    # ۱. فرستادن اطلاعات پست و کامنت‌های قبلی به قالب HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # پیدا کردن پستی که کاربر روی آن کلیک کرده بر اساس id
        post_obj = get_object_or_404(Post, id=self.kwargs["post_id"])
        context["post"] = post_obj
        # گرفتن تمام کامنت‌های مربوط به این پست
        context["comments"] = post_obj.comments.all().order_by("-created_at")
        return context

    # ۲. ثبت خودکار کاربر و پست برای کامنت جدید
    def form_valid(self, form):
        post_obj = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.post = post_obj
        form.instance.user = (
            self.request.user.profile
        )  # متصل کردن به پروفایل کاربر لاگین شده
        return super().form_valid(form)

    # ۳. ریدایرکت به همین صفحه پس از ارسال موفقیت‌آمیز کامنت
    def get_success_url(self):
        return reverse("posts:post_comments", kwargs={"post_id": self.kwargs["post_id"]})