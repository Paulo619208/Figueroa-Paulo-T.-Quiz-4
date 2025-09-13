import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.email} on {self.created_at}"

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.content[:50] or "post")
            unique_slug = base_slug
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{uuid.uuid4().hex[:4]}'
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def comment_count(self):
        return self.comment_set.count()

    @property
    def like_count(self):
        return self.like_set.count()

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.email} on {self.post}'

# ✅ ADDED: The Like model
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'Like by {self.user.email} on {self.post}'