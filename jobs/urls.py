from django.urls import path
from .views import job_list_view, job_detail_view, JobUpdateView, JobDeleteView, job_apply, JobCreateView

app_name = 'jobs'

urlpatterns = [

    path('', job_list_view, name='list'),
    path('create/', JobCreateView.as_view(), name='create'),
    path('<int:pk>/', job_detail_view, name='detail'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='delete'),
    path('<int:pk>/apply/', job_apply, name='apply'),
]