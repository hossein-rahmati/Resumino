
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Resume
from .forms import ResumeForm

@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user  # کاربر فعلی را به رزومه نسبت می‌دهیم
            resume.save()
            messages.success(request, 'رزومه با موفقیت ساخته شد!')
            return redirect('dashboard:resume_list')  # برگشت به لیست داشبورد
    else:
        form = ResumeForm()
    
    return render(request, 'resume_builder/resume_form.html', {
        'form': form,
        'title': 'ساخت رزومه جدید'
    })

@login_required
def resume_edit(request, pk):
    # فقط رزومه‌ای را بگیر که متعلق به کاربر فعلی باشد
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'رزومه با موفقیت ویرایش شد!')
            return redirect('dashboard:resume_list')
    else:
        form = ResumeForm(instance=resume)
    
    return render(request, 'resume_builder/resume_form.html', {
        'form': form,
        'title': 'ویرایش رزومه'
    })

@login_required
def resume_detail(request, pk):
    # فقط رزومه‌ی خود کاربر یا رزومه‌های عمومی (اگر اجازه بدید)
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resume_builder/resume_detail.html', {
        'resume': resume
    })

@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'رزومه با موفقیت حذف شد!')
        return redirect('dashboard:resume_list')
    
    return render(request, 'resume_builder/resume_confirm_delete.html', {
        'resume': resume
    })
# Create your views here.
