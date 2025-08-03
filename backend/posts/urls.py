from django.urls import path
from . import views

urlpatterns = [
    path('csrf-token/', views.csrf_token_view, name='csrf-token'),
    path('posts/', views.PostListCreateView.as_view(), name='posts'),
    path('posts/user/<str:username>/', views.UserPostsView.as_view(), name='user-posts'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.user_profile_view, name='user-profile'),
]
