from django.urls import path
from .views import signin_view, profile_view, logout_view, signup_view, profile_edit_view  # Renamed for clarity

app_name = 'auth'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('signout/', logout_view, name='signout'),

    # URL for viewing the user's own profile
    path('profile/', profile_view, name='profile'),

    # URL for editing the user's own profile
    path('profile/edit/', profile_edit_view, name='profile_edit'),
]