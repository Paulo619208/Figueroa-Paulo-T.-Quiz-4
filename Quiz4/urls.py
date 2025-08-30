"""
URL configuration for Quiz4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# This is the main list of URL patterns for the entire project.
urlpatterns = [
    # 1. Django Admin Site
    path('admin/', admin.site.urls),

    # 2. Authentication URLs (for login, logout, registration)
    # Any URL starting with 'auth/' will be handled by the 'accounts' app.
    path('auth/', include('accounts.urls', namespace='auth')),

    # 3. Job-related URLs
    # Any URL starting with 'jobs/' will be handled by the 'jobs' app.
    path('jobs/', include('jobs.urls', namespace='jobs')),

    # 4. Post-related URLs (for the main part of your site)
    # The root URL ('') will be handled by the 'posts' app. This is often your homepage.
    path('', include('posts.urls', namespace='posts')),
]

# This part is for serving static and media files during development ONLY.
# It allows your CSS, JavaScript, and user-uploaded images to work correctly.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)