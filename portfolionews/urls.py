from django.urls import path
from .views import IndexView

# from .feeds import RssArticlesFeeds
# from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # At first I wanted to implement a simple way to view articles, but I decided to postpone it for now
    # path('articles/', ArticleListView.as_view(), name='article_list'),
    # path('articles/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
]
