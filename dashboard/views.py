from django.shortcuts import render

# Create your views here.
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')
def my_resume_view(request):
    return render(request, 'dashboard/my_resume.html')
def template_view(request):
    return render(request,'dashboard/template.html')
def jobs_view(request):
    return render(request,'dashboard/jobs.html')
def submissions_view(request):
    return render(request,'dashboard/submissions.html')
