from django.urls import path
from .views import (
   NewsList,
   NewsDetail,
   NewsSearch,
   NewsCreate,
   NewsUpdate,
   NewsDelete,
   ArticleList,
   ArticleDetail,
   ArticleSearch,
   ArticleCreate,
   ArticleUpdate,
   ArticleDelete
)

urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('news/search/', NewsSearch.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/', ArticleList.as_view(), name='article_list'),
   path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
   path('articles/search/', ArticleSearch.as_view(), name='article_search'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
