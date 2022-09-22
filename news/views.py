from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, news, article
from .filters import PostFilter
from .forms import PostForm


class HomePage(TemplateView):
    template_name = 'homepage.html'


class NewsList(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    queryset = Post.objects.filter(type=news)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'

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
    template_name = 'news.html'
    context_object_name = 'news'
    permission_required = 'news.view_post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
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
    template_name = 'news_edit.html'
    permission_required = 'news.change_post'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'


class ArticleList(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'article_list.html'
    context_object_name = 'article_list'
    queryset = Post.objects.filter(type=article)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs


class ArticleSearch(ListView):
    model = Post
    template_name = 'article_search.html'

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
    template_name = 'article.html'
    context_object_name = 'article'
    permission_required = 'news.view_post'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
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
    template_name = 'article_edit.html'
    permission_required = 'news.change_post'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'news.delete_post'
