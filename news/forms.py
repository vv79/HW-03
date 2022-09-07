from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    categories = forms.SelectMultiple(
        choices=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

