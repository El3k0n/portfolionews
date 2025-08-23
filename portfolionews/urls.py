from .views import IndexView, ArticleListView, ArticleDetailView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
]
