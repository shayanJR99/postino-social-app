from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ( "author","content",  "is_edited",  "created_at")
admin.site.register(Post, PostAdmin)

