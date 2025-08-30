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
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    context = {
        'object_list': jobs,  # Use 'object_list' to match the template
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


# ✅ FIXED: Completed the JobCreateView with all required settings and security.
class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:list')

    # This test ensures only staff members can access this page
    def test_func(self):
        return self.request.user.is_staff

    # This automatically sets the job creator to the logged-in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'  # Can reuse the create form template

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.user or self.request.user.is_staff

    def get_success_url(self):
        # ✅ FIXED: Corrected the URL name from 'job_detail_view' to 'detail'
        return reverse_lazy('jobs:detail', kwargs={'pk': self.object.pk})


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_delete.html'
    # ✅ FIXED: Corrected the URL name from 'job_list_view' to 'list'
    success_url = reverse_lazy('jobs:list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.user or self.request.user.is_staff


def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # This should ideally redirect to login, but for now, this is fine
            return redirect('auth:signin')

        # Check if the user has already applied
        if JobApplicant.objects.filter(job=job, user=request.user).exists():
            messages.error(request, 'You have already applied for this job.')
            return redirect('jobs:detail', pk=job.pk)

        # Assuming your JobForm handles the resume upload
        # For simplicity, let's create the applicant directly
        JobApplicant.objects.create(job=job, user=request.user)
        messages.success(request, 'Application submitted successfully!')
        return redirect('jobs:detail', pk=job.pk)

    # This view is for POST requests, should redirect if accessed via GET
    return redirect('jobs:detail', pk=job.pk)