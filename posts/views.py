from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


# ✅ IMPROVED: Made this view require a login using the standard mixin for consistency.
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'


class PostDetailSlugView(DetailView):
    queryset = Post.objects.all()
    template_name = 'posts/post_detail.html'


# ✅ IMPROVED: Added LoginRequiredMixin for consistency.
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    # ✅ FIXED: success_url must use reverse_lazy to find the URL name correctly.
    success_url = reverse_lazy('posts:post-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post.")
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # ✅ FIXED: Added the required model, form, and template attributes.
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to edit this post.")
        return obj

    def get_success_url(self):
        return reverse_lazy('posts:post-detail', kwargs={'slug': self.object.slug})


# ✅ IMPROVED: Added LoginRequiredMixin to ensure only logged-in users can create posts.
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:post-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)