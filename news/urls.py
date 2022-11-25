from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .views import (
   HomePage,
   TimeZone,
   NewsList,
   NewsCategorySubscribe,
   NewsCategoryUnsubscribe,
   NewsDetail,
   NewsSearch,
   NewsCreate,
   NewsUpdate,
   NewsDelete,
   ArticleList,
   ArticleCategorySubscribe,
   ArticleCategoryUnsubscribe,
   ArticleDetail,
   ArticleSearch,
   ArticleCreate,
   ArticleUpdate,
   ArticleDelete
)

urlpatterns = [
   path('', HomePage.as_view(), name='homepage'),
   path('set/timezone/', TimeZone.as_view(), name='set_timezone'),

   path('news/', NewsList.as_view(), name='news_list'),
   path('news/category/<int:category>', NewsList.as_view(), name='news_category'),
   path('news/category/<int:category>/subscribe', login_required(NewsCategorySubscribe.as_view()), name='news_category_subscribe'),
   path('news/category/<int:category>/unsubscribe', login_required(NewsCategoryUnsubscribe.as_view()), name='news_category_unsubscribe'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('news/search/', NewsSearch.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/', ArticleList.as_view(), name='article_list'),
   path('articles/category/<int:category>', ArticleList.as_view(), name='article_category'),
   path('articles/category/<int:category>/subscribe', login_required(ArticleCategorySubscribe.as_view()), name='article_category_subscribe'),
   path('articles/category/<int:category>/unsubscribe', login_required(ArticleCategoryUnsubscribe.as_view()), name='article_category_unsubscribe'),
   path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
   path('articles/search/', ArticleSearch.as_view(), name='article_search'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
