from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'date_created')
    date_hierarchy = 'date_created'
