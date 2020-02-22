from django.urls import path
from . import views
from .views import PostListView, PostDetail,PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/',PostDetail.as_view(),name = 'post-detail'), #here i want to have comments
    path('post/new/',PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
