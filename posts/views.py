from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
# ✅ 1. IMPORT THE NEW MODELS AND FORMS
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


# ✅ 2. ADD THIS NEW VIEW TO HANDLE LIKES
def toggle_like(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    # Order posts by newest first
    queryset = Post.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get a set of post slugs that the current user has liked
        liked_posts = Like.objects.filter(user=self.request.user).values_list('post__slug', flat=True)
        context['liked_posts'] = set(liked_posts)
        return context


# ✅ 3. UPDATE THIS VIEW TO HANDLE COMMENTS
class PostDetailSlugView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = Comment.objects.filter(post=post).order_by('-created_at')
        context['comment_form'] = CommentForm()
        if self.request.user.is_authenticated:
            context['user_has_liked'] = Like.objects.filter(post=post, user=self.request.user).exists()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:signin')

        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts:post-detail', slug=post.slug)
        else:
            # If the form is invalid, re-render the page with the form and its errors
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post.")
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
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


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:post-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)