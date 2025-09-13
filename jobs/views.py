from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import JobForm
from .models import Job, JobApplicant


def job_list_view(request):
    jobs = Job.objects.all()
    query = request.GET.get('q', None)
    if query:
        # ✅ FIXED: Changed field names to match your Job model (e.g., 'title' -> 'job_title')
        jobs = jobs.filter(
            Q(job_title__icontains=query) |
            Q(job_description__icontains=query) |
            Q(location__icontains=query)
        )
    context = {
        'object_list': jobs,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applicants = JobApplicant.objects.filter(job=job)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplicant.objects.filter(job=job, user=request.user).exists()

    context = {
        'job': job,
        'applicants': applicants,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('jobs:detail', kwargs={'pk': self.object.pk})


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_delete.html'
    success_url = reverse_lazy('jobs:list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.user or self.request.user.is_staff


def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('auth:signin')

        if JobApplicant.objects.filter(job=job, user=request.user).exists():
            messages.error(request, 'You have already applied for this job.')
            return redirect('jobs:detail', pk=job.pk)

        JobApplicant.objects.create(job=job, user=request.user)
        messages.success(request, 'Application submitted successfully!')
        return redirect('jobs:detail', pk=job.pk)

    return redirect('jobs:detail', pk=job.pk)