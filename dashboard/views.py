from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')
@login_required
def account_settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'اطلاعات حساب کاربری با موفقیت به‌روز شد.')
            return redirect('account_settings')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'dashboard/account_settings.html', context)
def my_resume_view(request):
    return render(request, 'dashboard/my_resume.html')
def template_view(request):
    return render(request,'dashboard/template.html')
def jobs_view(request):
    return render(request,'dashboard/jobs.html')
def submissions_view(request):
    return render(request,'dashboard/submissions.html')
