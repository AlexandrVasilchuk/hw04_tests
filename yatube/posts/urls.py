from django.urls import path

from posts import views
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.post_create, name='post_create'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path(
        'posts/<int:post_id>/comment/', views.add_comment, name='add_comment'
    ),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
