from django.contrib import admin
from .models import Post


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
    nullify_rating.short_description = 'Nullify rating'


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'rating', 'date_created')
    list_filter = ('title', 'type', 'author', 'rating', 'date_created')
    search_fields = ('title', 'author__user__first_name', 'author__user__last_name', 'author__user__username')
    actions = [nullify_rating]
    date_hierarchy = 'date_created'
