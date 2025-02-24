from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostListView, PostCreateView, PostDetailView, PostDeleteView, PostUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('details/<int:pk>/', PostDetailView.as_view(), name='post_details'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('create', PostCreateView.as_view(), name='post_create'),
]