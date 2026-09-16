import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from accounts.models import Profile
from .models import Resume, JobListing, JobSubmission, SavedJob


def ensure_seed_jobs():
    """Ensure standard popular tech job listings exist in the database."""
    if JobListing.objects.exists():
        return
    
    sample_jobs = [
        {
            "title": "برنامه‌نویس ارشد Python / Django",
            "company_name": "دیجی‌کالا (Digikala)",
            "company_initial": "د",
            "company_logo_color": "red",
            "location": "تهران (امکان دورکاری)",
            "job_type": "تمام وقت",
            "work_mode": "امکان دورکاری (هیبریدی)",
            "salary_range": "۴۵ تا ۶۵ میلیون تومان",
            "experience_level": "Senior (۳+ سال)",
            "category": "برنامه‌نویسی و نرم‌افزار",
            "skills_required": "Python, Django, PostgreSQL, Redis, Docker, Celery",
            "description": "توسعه و نگهداری سرویس‌های مقیاس‌پذیر در پلتفرم خرید آنلاین دیجی‌کالا، کار با پایگاه‌های داده توزیع‌شده و سیستم‌های صف پیام.",
            "benefits": "بیمه تکمیلی SOS، ناهار، کمک‌هزینه یادگیری، ساعت کاری منعطف، پاداش عملکرد",
            "is_featured": True,
            "is_urgent": True,
        },
        {
            "title": "توسعه‌دهنده Backend (Python / FastAPI)",
            "company_name": "اسنپ (Snapp!)",
            "company_initial": "ا",
            "company_logo_color": "emerald",
            "location": "تهران",
            "job_type": "تمام وقت",
            "work_mode": "امکان دورکاری (هیبریدی)",
            "salary_range": "۴۰ تا ۵۵ میلیون تومان",
            "experience_level": "Mid-Level (۲+ سال)",
            "category": "برنامه‌نویسی و نرم‌افزار",
            "skills_required": "Python, FastAPI, Kafka, Docker, Kubernetes, MongoDB",
            "description": "طراحی و بهینه‌سازی میکروسرویس‌های حمل‌ونقل و پرداخت اسنپ با کارایی بالا و زمان پاسخ‌دهی میلی‌ثانیه‌ای.",
            "benefits": "بیمه تکمیلی، بن خرید اسنپ‌فود، سهام تشویقی، ارتقای شغلی سریع",
            "is_featured": True,
            "is_urgent": False,
        },
        {
            "title": "برنامه‌نویس فرانت‌اند React / Next.js",
            "company_name": "کافه‌بازار (Bazaar)",
            "company_initial": "ک",
            "company_logo_color": "emerald",
            "location": "دورکاری کامل",
            "job_type": "تمام وقت",
            "work_mode": "دورکاری کامل",
            "salary_range": "۳۵ تا ۵۰ میلیون تومان",
            "experience_level": "Mid-Level",
            "category": "فرانت‌اند و طراحی وب",
            "skills_required": "React.js, Next.js, TypeScript, Tailwind CSS, Redux Toolkit",
            "description": "پیاده‌سازی پنل‌های پیشرفته و رابط‌های کاربری وب‌اپلیکیشن کافه‌بازار با تمرکز بر Performance و UX بی‌نقص.",
            "benefits": "امکان کار ۱۰۰٪ ریموت، تجهیزات کامل کاری، بیمه سامان، کمک هزینه سلامت روان",
            "is_featured": False,
            "is_urgent": True,
        },
        {
            "title": "متخصص DevOps و زیرساخت ابری",
            "company_name": "نوبیتکس (Nobitex)",
            "company_initial": "ن",
            "company_logo_color": "blue",
            "location": "تهران",
            "job_type": "تمام وقت",
            "work_mode": "امکان دورکاری (هیبریدی)",
            "salary_range": "۵۰ تا ۷۰ میلیون تومان",
            "experience_level": "Senior (۴+ سال)",
            "category": "دواپس و زیرساخت",
            "skills_required": "Linux, Kubernetes, Docker, CI/CD, Prometheus, Grafana, Ansible",
            "description": "مدیریت و نگهداری خوشه‌های کوبرنتیز در محیط پروداکشن صرافی ارز دیجیتال با امنیت بسیار بالا و دسترس‌پذیری ۹۹.۹۹٪.",
            "benefits": "پاداش‌های فصلی کریپتویی، بیمه تکمیلی، فضای بازی، ناهار ارگانیک",
            "is_featured": True,
            "is_urgent": False,
        },
        {
            "title": "طراح ارشد رابط و تجربه کاربری (UI/UX Designer)",
            "company_name": "علی‌بابا (Alibaba Travels)",
            "company_initial": "ع",
            "company_logo_color": "amber",
            "location": "تهران (سعادت‌آباد)",
            "job_type": "تمام وقت",
            "work_mode": "حضوری",
            "salary_range": "۳۰ تا ۴۵ میلیون تومان",
            "experience_level": "Mid-Level / Senior",
            "category": "طراحی محصول و UI/UX",
            "skills_required": "Figma, Design Systems, User Research, Wireframing, Prototyping",
            "description": "طراحی جریان‌های رزرو پرواز و هتل، ایجاد کامپوننت‌های سیستم طراحی و انجام تست‌های کاربردپذیری با مشتریان واقعی.",
            "benefits": "تخفیف‌های ویژه سفرهای داخلی و خارجی، وام خرید تجهیزات، باشگاه ورزشی",
            "is_featured": False,
            "is_urgent": False,
        },
        {
            "title": "کارشناس هوش مصنوعی و پردازش زبان طبیعی (NLP / LLM)",
            "company_name": "تپسی (Tapsi)",
            "company_initial": "ت",
            "company_logo_color": "orange",
            "location": "تهران",
            "job_type": "تمام وقت",
            "work_mode": "امکان دورکاری (هیبریدی)",
            "salary_range": "۴۵ تا ۶۰ میلیون تومان",
            "experience_level": "Senior",
            "category": "هوش مصنوعی و داده",
            "skills_required": "Python, PyTorch, LangChain, Transformers, RAG, OpenAI / Groq API",
            "description": "توسعه چت‌بات‌ها و سیستم‌های پردازش هوشمند درخواست‌ها و تطبیق الگوریتم‌های پیشنهاد هوشمند سفر.",
            "benefits": "فرصت‌های تحقیقاتی، دسترسی به سرورهای GPU قدرتمند، بیمه درجه یک",
            "is_featured": True,
            "is_urgent": True,
        },
    ]

    for data in sample_jobs:
        JobListing.objects.create(**data)


def ensure_starter_data_for_user(user):
    """Ensure user has profile, a primary resume, and sample submissions if brand new."""
    Profile.objects.get_or_create(user=user)
    ensure_seed_jobs()

    if not Resume.objects.filter(user=user).exists():
        first_resume = Resume.objects.create(
            user=user,
            title="رزومه اصلی - برنامه‌نویس وب",
            target_job="توسعه‌دهنده فول‌استک پایتون و جنگو",
            template_name="modern",
            theme_color="blue",
            language="fa",
            summary="برنامه‌نویس علاقه‌مند و باانگیزه با تسلط بر پایتون، جنگو و پایگاه‌های داده رابطه‌ای. تجربه در طراحی REST API، ساخت سیستم‌های مقیاس‌پذیر و همکاری در تیم‌های چابک (Agile).",
            skills="Python, Django, Django REST Framework, PostgreSQL, Docker, Git, Redis, Tailwind CSS",
            completion_percentage=85,
            ats_score=88,
            views_count=5,
            downloads_count=2,
            is_primary=True,
        )

        # Create initial submission if jobs exist
        first_job = JobListing.objects.first()
        if first_job:
            JobSubmission.objects.create(
                user=user,
                job=first_job,
                company_name=first_job.company_name,
                job_title=first_job.title,
                resume=first_resume,
                status="reviewing",
                note="رزومه توسط مدیر فنی مشاهده شده و برای مرحله بررسی اولیه ارسال شد.",
            )


@login_required
def dashboard_view(request):
    user = request.user
    ensure_starter_data_for_user(user)

    profile, _ = Profile.objects.get_or_create(user=user)
    resumes = Resume.objects.filter(user=user)
    primary_resume = resumes.filter(is_primary=True).first() or resumes.first()
    
    submissions = JobSubmission.objects.filter(user=user)[:5]
    featured_jobs = JobListing.objects.filter(is_featured=True)[:4]
    
    total_resumes = resumes.count()
    total_views = sum(r.views_count for r in resumes)
    total_submissions = JobSubmission.objects.filter(user=user).count()
    active_interviews = JobSubmission.objects.filter(user=user, status="interview").count()
    
    # Calculate average ATS score
    avg_ats = round(sum(r.ats_score for r in resumes) / total_resumes) if total_resumes else 80

    context = {
        "profile": profile,
        "resumes": resumes,
        "primary_resume": primary_resume,
        "submissions": submissions,
        "featured_jobs": featured_jobs,
        "total_resumes": total_resumes,
        "total_views": total_views,
        "total_submissions": total_submissions,
        "active_interviews": active_interviews,
        "avg_ats": avg_ats,
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def my_resume_view(request):
    return render(request, 'dashboard/my_resume.html')
def template_view(request):
    return render(request,'dashboard/template.html')
def jobs_view(request):
    return render(request,'dashboard/jobs.html')
def submissions_view(request):
    return render(request,'dashboard/submissions.html')
