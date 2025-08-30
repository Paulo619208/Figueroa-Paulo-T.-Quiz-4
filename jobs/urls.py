from django.urls import path
from .views import job_list_view, job_detail_view, JobUpdateView, JobDeleteView, job_apply, JobCreateView

app_name = 'jobs'

urlpatterns = [
    # Using shorter names makes them easier to call from templates
    # e.g., {% url 'jobs:list' %} instead of {% url 'jobs:job_list_view' %}
    path('', job_list_view, name='list'),
    path('create/', JobCreateView.as_view(), name='create'),
    path('<int:pk>/', job_detail_view, name='detail'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='delete'),
    path('<int:pk>/apply/', job_apply, name='apply'),
]