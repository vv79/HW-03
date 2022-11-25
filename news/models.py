from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import textwrap
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

POST_PREVIEW_LENGTH = 124

article = 'ART'
news = 'NEWS'

POST_TYPES = [
    (article, 'Article'),
    (news, 'News')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(postRating=Sum('rating'))
        post_rating = 0
        post_rating += posts_rating.get('postRating')

        comments_rating = self.user.comment_set.aggregate(commentRating=Sum('rating'))

        comment_rating = 0
        comment_rating += comments_rating.get('commentRating')

        self.rating = post_rating * 3 + comment_rating
        self.save()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')

    def __str__(self):
        return self.name


class CategorySubscriber(models.Model):
    type = models.CharField(max_length=8, choices=POST_TYPES, default=article)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "news_category_subscriber"


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=POST_TYPES, default=article)
    date_created = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, )
    content = models.TextField()
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        return textwrap.shorten(self.content, width=POST_PREVIEW_LENGTH, placeholder='...')

    def __str__(self):
        return f'{self.date_created.strftime("%Y-%m-%d %H:%M:%S")}|{self.author.user.username}|{self.rating}|{self.title}: {self.preview}'

    def get_absolute_url(self):
        return reverse('article_detail' if type == article else 'news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.date_created.strftime("%Y-%m-%d %H:%M:%S")}|{self.user.username}|{self.rating}|{self.content}'
