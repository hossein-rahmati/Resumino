from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Profile, Resume, Submission
from dashboard.forms import ResumeForm, SubmissionForm, CommentForm

def calculate_completion(user):
    score = 0
    if user.first_name and user.last_name:
        score += 20
    if hasattr(user, 'profile') and user.profile.job_title:
        score += 15
    if hasattr(user, 'profile') and user.profile.phone:
        score += 10
    if hasattr(user, 'profile') and user.profile.location:
        score += 10
    
    resumes = Resume.objects.filter(user=user)
    for resume in resumes:
        if resume.experience:  # ← changed from experiences
            score += 20
            break
    for resume in resumes:
        if resume.education:   # ← changed from educations
            score += 15
            break
    for resume in resumes:
        if resume.skills:
            score += 10
            break
    
    return min(score, 100)


@login_required
def dashboard_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        messages.info(request, 'پروفایل شما به‌طور خودکار ساخته شد. لطفاً اطلاعات را کامل کنید.')

    resumes = Resume.objects.filter(user=user)
    submissions = Submission.objects.filter(user=user)

    context = {
        'has_profile': bool(user.first_name or user.last_name or profile.job_title),
        'resume_count': resumes.count(),
        'submission_count': submissions.count(),
        'latest_resume': resumes.order_by('-created_at').first(),
        'latest_submission': submissions.order_by('-created_at').first(),
        'resume_completion': calculate_completion(user),
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def account_settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, 'پروفایل شما به‌طور خودکار ساخته شد. لطفاً اطلاعات را کامل کنید.')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'اطلاعات حساب کاربری با موفقیت به‌روز شد.')
            return redirect('account_settings')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'dashboard/account_settings.html', context)


@login_required
def my_resume_view(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard/my_resume.html', {'resumes': resumes})


@login_required
def template_view(request):
    return render(request, 'dashboard/templates.html')


@login_required
def jobs_view(request):
    return render(request, 'dashboard/jobs.html')


@login_required
def submissions_view(request):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, 'dashboard/submissions.html', {'submissions': submissions})