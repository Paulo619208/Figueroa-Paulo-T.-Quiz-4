from django.urls import path
# ✅ 1. IMPORT THE NEW toggle_like VIEW
from .views import (
    PostListView,
    PostDetailSlugView,
    PostDeleteView,
    PostUpdateView,
    PostCreateView,
    toggle_like
)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),

    # ✅ 2. ADD THE NEW URL FOR LIKING POSTS
    path('like/<slug:slug>/', toggle_like, name='toggle-like'),

    path('<str:slug>/', PostDetailSlugView.as_view(), name='post-detail'),
    path('<str:slug>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('<str:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
]