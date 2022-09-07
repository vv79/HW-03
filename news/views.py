from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Post, news, article, POST_TYPES
from .filters import PostFilter
from .forms import PostForm


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


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        author = Author.objects.get(user__username='ivanov')
        post = form.save(commit=False)
        post.type = news
        post.author = author
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


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


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        author = Author.objects.get(user__username='petrov')
        post = form.save(commit=False)
        post.type = article
        post.author = author
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
