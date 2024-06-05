from django.urls import path

from mainapp.views import ArticleListView, AboutView, ArticleDetailView, EditArticleView, DeleteArticleView, CommentDeleteView, ContactView, CreateArticleView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('create_article/', CreateArticleView.as_view(), name='create_article'),
    path('category_filter/<int:category_id>', ArticleListView.as_view(), name='category_filter'),
    path('edit_article/<int:pk>', EditArticleView.as_view(), name='edit_article'),
    path('delete_article/<int:pk>', DeleteArticleView.as_view(), name='delete_article'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
]
