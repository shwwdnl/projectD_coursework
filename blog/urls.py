from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import BlogConfig
from .views import ArticleListView, ArticleCreateView, ArticleUpdateView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name='blog_list'),
    path("article/<int:pk>", cache_page(60)(ArticleDetailView.as_view()), name='article_detail'),
    path("create/", ArticleCreateView.as_view(), name='article_create'),
    path("edit/<int:pk>", ArticleUpdateView.as_view(), name='article_edit'),
]
