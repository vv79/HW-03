from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from .models import Post, Category, CategorySubscriber, news, article
from .filters import PostFilter
from .forms import PostForm
from django.contrib import messages
from django.http import Http404


class HomePage(TemplateView):
    template_name = 'homepage.html'


class NewsList(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    queryset = Post.objects.filter(type=news)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category')

        context['category'] = None
        context['already_subscribed'] = False

        if category_id:
            user = self.request.user
            category = Category.objects.get(id=category_id)
            context['category'] = category
            if user.is_authenticated:
                context['already_subscribed'] = CategorySubscriber.objects.filter(type=news, category=category, user=user).exists()

        context['filter'] = self.filter
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category')
        if category_id:
            queryset = Post.objects.filter(type=news, categories=category_id)
        else:
            queryset = super().get_queryset()

        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs


class NewsCategorySubscribe(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        category = Category.objects.get(id=self.kwargs.get('category'))

        if not category or not user.is_authenticated:
            raise Http404

        category_subscriber = CategorySubscriber.objects.filter(type=news, category=category.id, user=user.id).first()

        if not category_subscriber:
            subscriber = CategorySubscriber.objects.create(type=news, category=category, user=user)
            subscriber.save()

            messages.success(request, "Congratulations, you are now subscribed to news in this category.")
        else:
            messages.error(request, "You are already subscribed to news in this category.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('news_category', category=kwargs.get('category'))


class NewsCategoryUnsubscribe(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        category = Category.objects.get(id=self.kwargs.get('category'))

        if not category:
            raise Http404

        category_subscriber = CategorySubscriber.objects.filter(type=news, category=category.id, user=user.id).first()

        if category_subscriber:
            category_subscriber.delete()

            messages.success(request, "Congratulations, you are now unsubscribed to news in this category.")
        else:
            messages.error(request, "You are not subscribed to news in this category.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('news_category', category=kwargs.get('category'))


class NewsSearch(ListView):
    model = Post
    template_name = 'news/news_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs


class NewsDetail(PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    permission_required = 'news.view_post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        author = self.request.user
        post = form.save(commit=False)
        post.type = news
        post.author = author
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    permission_required = 'news.change_post'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'


class ArticleList(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'news/article_list.html'
    context_object_name = 'article_list'
    queryset = Post.objects.filter(type=article)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category')

        context['category'] = None
        context['already_subscribed'] = False

        if category_id:
            user = self.request.user
            category = Category.objects.get(id=category_id)
            context['category'] = category
            if user.is_authenticated:
                context['already_subscribed'] = CategorySubscriber.objects.filter(type=article, category=category, user=user).exists()

        context['filter'] = self.filter
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category')
        if category_id:
            queryset = Post.objects.filter(type=article, categories=category_id)
        else:
            queryset = super().get_queryset()

        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs


class ArticleCategorySubscribe(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        category = Category.objects.get(id=self.kwargs.get('category'))

        if not category:
            raise Http404

        category_subscriber = CategorySubscriber.objects.filter(type=article, category=category.id, user=user.id).first()

        if not category_subscriber:
            subscriber = CategorySubscriber.objects.create(type=article, category=category, user=user)
            subscriber.save()

            messages.success(request, "Congratulations, you are now subscribed to articles in this category.")
        else:
            messages.error(request, "You are already subscribed to articles in this category.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('article_category', category=kwargs.get('category'))


class ArticleCategoryUnsubscribe(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        category = Category.objects.get(id=self.kwargs.get('category'))

        if not category:
            raise Http404

        category_subscriber = CategorySubscriber.objects.filter(type=article, category=category.id, user=user.id).first()

        if category_subscriber:
            category_subscriber.delete()

            messages.success(request, "Congratulations, you are now unsubscribed to articles in this category.")
        else:
            messages.error(request, "You are not subscribed to articles in this category.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('article_category', category=kwargs.get('category'))


class ArticleSearch(ListView):
    model = Post
    template_name = 'news/article_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs


class ArticleDetail(PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'news/article.html'
    context_object_name = 'article'
    permission_required = 'news.view_post'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        author = self.request.user
        post = form.save(commit=False)
        post.type = article
        post.author = author
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_edit.html'
    permission_required = 'news.change_post'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'news.delete_post'
