import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    # Use settings.AUTH_USER_MODEL for better portability
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # ✅ FIXED: Simplified the image upload path. Django handles unique filenames.
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # ✅ FIXED: Made slug blank=True to allow it to be auto-generated
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Using email is safer if your custom user model doesn't have a username
        return f"Post by {self.user.email} on {self.created_at}"

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.slug})

    # ✅ FIXED: Added logic to automatically create a unique slug before saving
    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a base slug from the first 50 characters of content
            base_slug = slugify(self.content[:50] or "post")

            # Ensure the slug is unique by appending a short unique ID if needed
            unique_slug = base_slug
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{uuid.uuid4().hex[:4]}'
            self.slug = unique_slug
        super().save(*args, **kwargs)