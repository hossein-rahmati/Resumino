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
    user = request.user
    ensure_starter_data_for_user(user)

    profile, _ = Profile.objects.get_or_create(user=user)
    resumes = Resume.objects.filter(user=user)
    primary_resume = resumes.filter(is_primary=True).first() or resumes.first()

    context = {
        "profile": profile,
        "resumes": resumes,
        "primary_resume": primary_resume,
        "theme_colors": Resume.THEME_COLORS,
        "templates": Resume.TEMPLATES,
    }
    return render(request, "dashboard/my_resume.html", context)


@login_required
def create_resume_view(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip() or "رزومه جدید"
        target_job = request.POST.get("target_job", "").strip()
        template_name = request.POST.get("template_name", "modern")
        theme_color = request.POST.get("theme_color", "blue")
        language = request.POST.get("language", "fa")
        summary = request.POST.get("summary", "").strip()
        skills = request.POST.get("skills", "").strip() or "Python, Django, Git"
        is_primary = request.POST.get("is_primary") == "on"

        if is_primary:
            Resume.objects.filter(user=request.user).update(is_primary=False)

        resume = Resume.objects.create(
            user=request.user,
            title=title,
            target_job=target_job,
            template_name=template_name,
            theme_color=theme_color,
            language=language,
            summary=summary,
            skills=skills,
            completion_percentage=80,
            ats_score=85,
            is_primary=is_primary or (Resume.objects.filter(user=request.user).count() == 1),
        )
        messages.success(request, f"رزومه «{resume.title}» با موفقیت ایجاد شد.")
        return redirect("my_resume")

    return redirect("my_resume")


@login_required
def edit_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == "POST":
        resume.title = request.POST.get("title", resume.title).strip()
        resume.target_job = request.POST.get("target_job", resume.target_job).strip()
        resume.template_name = request.POST.get("template_name", resume.template_name)
        resume.theme_color = request.POST.get("theme_color", resume.theme_color)
        resume.language = request.POST.get("language", resume.language)
        resume.summary = request.POST.get("summary", resume.summary).strip()
        resume.skills = request.POST.get("skills", resume.skills).strip()

        # Recalculate completion score
        score = 40
        if resume.target_job: score += 15
        if resume.summary: score += 20
        if resume.skills: score += 15
        if request.user.first_name and request.user.last_name: score += 10
        resume.completion_percentage = min(score, 100)
        resume.ats_score = min(score + 5, 98)

        resume.save()
        messages.success(request, f"تغییرات رزومه «{resume.title}» ذخیره شد.")
        return redirect("my_resume")

    return redirect("my_resume")


@login_required
def delete_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        title = resume.title
        resume.delete()
        
        # If deleted resume was primary, set another one as primary
        remaining = Resume.objects.filter(user=request.user)
        if remaining.exists() and not remaining.filter(is_primary=True).exists():
            first = remaining.first()
            first.is_primary = True
            first.save()
            
        messages.success(request, f"رزومه «{title}» با موفقیت حذف شد.")
        return redirect("my_resume")
        
    return redirect("my_resume")


@login_required
def set_primary_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    Resume.objects.filter(user=request.user).update(is_primary=False)
    resume.is_primary = True
    resume.save()
    messages.success(request, f"رزومه «{resume.title}» به عنوان رزومه اصلی شما انتخاب شد.")
    return redirect("my_resume")


@login_required
def change_template_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == "POST":
        template_name = request.POST.get("template_name")
        theme_color = request.POST.get("theme_color")
        if template_name:
            resume.template_name = template_name
        if theme_color:
            resume.theme_color = theme_color
        resume.save()
        messages.success(request, f"قالب رزومه «{resume.title}» با موفقیت تغییر کرد.")
        return redirect("template")
    return redirect("template")


@login_required
def preview_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    # Increment view count
    resume.views_count += 1
    resume.save(update_fields=["views_count"])

    context = {
        "resume": resume,
        "profile": profile,
        "skills_list": resume.get_skills_list(),
    }
    return render(request, "dashboard/preview_resume.html", context)


@login_required
def template_view(request):
    user = request.user
    ensure_starter_data_for_user(user)

    profile, _ = Profile.objects.get_or_create(user=user)
    resumes = Resume.objects.filter(user=user)
    primary_resume = resumes.filter(is_primary=True).first() or resumes.first()

    templates_data = [
        {
            "id": "modern",
            "name": "Modern (مدرن)",
            "category": "tech",
            "badge": "محبوب‌ترین",
            "badge_color": "blue",
            "ats_friendly": True,
            "description": "قالب بسیار شیک و تمیز با بخش‌بندی مدرن و نوار کناری آیکون‌دار. مناسب برای متخصصان تکنولوژی، مهندسان نرم‌افزار و استارتاپ‌ها.",
            "popularity": "۹۸٪ رضایت کاربران",
        },
        {
            "id": "minimal",
            "name": "Minimal (مینیمال)",
            "category": "general",
            "badge": "تایید شده ATS",
            "badge_color": "emerald",
            "ats_friendly": True,
            "description": "طراحی مینیمال و خطی با حداکثر خوانایی و فضای سفید بهینه. بالاترین نرخ قبولی در سیستم‌های خودکار اسکن رزومه ATS شرکت‌های بین‌المللی.",
            "popularity": "۹۵٪ رضایت کاربران",
        },
        {
            "id": "executive",
            "name": "Executive (مدیران و رهبران)",
            "category": "management",
            "badge": "حرفه‌ای",
            "badge_color": "purple",
            "ats_friendly": True,
            "description": "ساختار سنگین، کلاسیک و پرستیژ بالا با هدر عریض و تاکید بر نتایج کلیدی، دستاوردها و مهارت‌های رهبری تیم.",
            "popularity": "۹۲٪ رضایت کاربران",
        },
        {
            "id": "tech_ats",
            "name": "Tech ATS (استاندارد نرم‌افزاری)",
            "category": "tech",
            "badge": "استاندارد جهانی",
            "badge_color": "indigo",
            "ats_friendly": True,
            "description": "طراحی تک‌ستونه بر اساس استاندارد شرکت‌های Big Tech مانند Google و Amazon. بهینه‌سازی شده برای هایلایت پروژه‌ها و مهارت‌های فنی.",
            "popularity": "۹۷٪ رضایت کاربران",
        },
        {
            "id": "creative",
            "name": "Creative (خلاقانه و دیزاین)",
            "category": "design",
            "badge": "جذاب و نوین",
            "badge_color": "rose",
            "ats_friendly": False,
            "description": "ترکیب رنگی چشم‌نواز، تایپوگرافی ویژه و چیدمان پویای بصری برای طراحان گرافیک، UI/UX، تدوین‌گران و مدیران مارکتینگ.",
            "popularity": "۹۰٪ رضایت کاربران",
        },
        {
            "id": "academic",
            "name": "Academic (آکادمیک و پژوهشی)",
            "category": "academic",
            "badge": "کامل و علمی",
            "badge_color": "slate",
            "ats_friendly": True,
            "description": "قالب فرمت CV استاندارد برای اساتید، پژوهشگران، پذیرش دانشگاه‌های خارجی و موسسات تحقیقاتی با بخش مقالات و افتخارات.",
            "popularity": "۸۹٪ رضایت کاربران",
        },
    ]

    context = {
        "profile": profile,
        "resumes": resumes,
        "primary_resume": primary_resume,
        "templates_data": templates_data,
    }
    return render(request, "dashboard/template.html", context)


@login_required
def jobs_view(request):
    user = request.user
    ensure_starter_data_for_user(user)

    profile, _ = Profile.objects.get_or_create(user=user)
    resumes = Resume.objects.filter(user=user)
    primary_resume = resumes.filter(is_primary=True).first() or resumes.first()

    # Search & Filters
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    work_mode = request.GET.get("work_mode", "")
    job_type = request.GET.get("job_type", "")
    
    jobs = JobListing.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(skills_required__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        jobs = jobs.filter(category=category)
    if work_mode:
        jobs = jobs.filter(work_mode=work_mode)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    saved_job_ids = list(SavedJob.objects.filter(user=user).values_list("job_id", flat=True))
    applied_job_ids = list(JobSubmission.objects.filter(user=user).values_list("job_id", flat=True))

    categories = JobListing.objects.values_list("category", flat=True).distinct()

    context = {
        "profile": profile,
        "resumes": resumes,
        "primary_resume": primary_resume,
        "jobs": jobs,
        "saved_job_ids": saved_job_ids,
        "applied_job_ids": applied_job_ids,
        "categories": categories,
        "query": query,
        "selected_category": category,
        "selected_work_mode": work_mode,
        "selected_job_type": job_type,
    }
    return render(request, "dashboard/jobs.html", context)


@login_required
def toggle_save_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    saved = SavedJob.objects.filter(user=request.user, job=job)
    
    if saved.exists():
        saved.delete()
        messages.info(request, f"موقعیت شغلی «{job.title}» از لیست نشان‌شده‌ها حذف شد.")
    else:
        SavedJob.objects.create(user=request.user, job=job)
        messages.success(request, f"موقعیت شغلی «{job.title}» با موفقیت نشان شد.")

    next_url = request.META.get("HTTP_REFERER", "jobs")
    return redirect(next_url)


@login_required
def apply_job_view(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    user = request.user
    
    if request.method == "POST":
        resume_id = request.POST.get("resume_id")
        note = request.POST.get("note", "").strip()

        resume = Resume.objects.filter(user=user, id=resume_id).first() if resume_id else Resume.objects.filter(user=user, is_primary=True).first()

        # Check if already applied
        existing = JobSubmission.objects.filter(user=user, job=job).first()
        if existing:
            messages.warning(request, f"شما قبلاً برای موقعیت «{job.title}» در شرکت {job.company_name} رزومه ارسال کرده‌اید.")
            return redirect("submissions")

        JobSubmission.objects.create(
            user=user,
            job=job,
            company_name=job.company_name,
            job_title=job.title,
            resume=resume,
            status="pending",
            note=note or "رزومه از طریق سامانه رزومینو ارسال شد.",
        )
        messages.success(request, f"رزومه شما با موفقیت برای موقعیت «{job.title}» در شرکت {job.company_name} ارسال شد!")
        return redirect("submissions")

    return redirect("jobs")


@login_required
def submissions_view(request):
    user = request.user
    ensure_starter_data_for_user(user)

    profile, _ = Profile.objects.get_or_create(user=user)
    resumes = Resume.objects.filter(user=user)
    
    status_filter = request.GET.get("status", "all")
    submissions = JobSubmission.objects.filter(user=user)

    if status_filter != "all":
        submissions = submissions.filter(status=status_filter)

    # Statistics
    all_count = JobSubmission.objects.filter(user=user).count()
    pending_count = JobSubmission.objects.filter(user=user, status="pending").count()
    reviewing_count = JobSubmission.objects.filter(user=user, status="reviewing").count()
    interview_count = JobSubmission.objects.filter(user=user, status="interview").count()
    accepted_count = JobSubmission.objects.filter(user=user, status="accepted").count()
    rejected_count = JobSubmission.objects.filter(user=user, status="rejected").count()

    context = {
        "profile": profile,
        "resumes": resumes,
        "submissions": submissions,
        "status_filter": status_filter,
        "all_count": all_count,
        "pending_count": pending_count,
        "reviewing_count": reviewing_count,
        "interview_count": interview_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
    }
    return render(request, "dashboard/submissions.html", context)


@login_required
def add_manual_submission_view(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name", "").strip()
        job_title = request.POST.get("job_title", "").strip()
        status = request.POST.get("status", "pending")
        resume_id = request.POST.get("resume_id")
        note = request.POST.get("note", "").strip()

        if not company_name or not job_title:
            messages.error(request, "لطفاً نام شرکت و عنوان شغلی را وارد نمایید.")
            return redirect("submissions")

        resume = Resume.objects.filter(user=request.user, id=resume_id).first() if resume_id else None

        JobSubmission.objects.create(
            user=request.user,
            company_name=company_name,
            job_title=job_title,
            status=status,
            resume=resume,
            note=note,
        )
        messages.success(request, f"درخواست شغلی مربوط به شرکت «{company_name}» با موفقیت در ترکر ثبت شد.")
        return redirect("submissions")

    return redirect("submissions")


@login_required
def update_submission_status_view(request, submission_id):
    submission = get_object_or_404(JobSubmission, id=submission_id, user=request.user)
    if request.method == "POST":
        new_status = request.POST.get("status")
        interview_time = request.POST.get("interview_time", "").strip()
        note = request.POST.get("note", "").strip()

        if new_status in dict(JobSubmission.STATUS_CHOICES):
            submission.status = new_status
        if interview_time:
            submission.interview_time = interview_time
        if note:
            submission.note = note
        
        submission.save()
        messages.success(request, f"وضعیت درخواست برای «{submission.company_name}» بروزرسانی شد.")
        return redirect("submissions")

    return redirect("submissions")


@login_required
def delete_submission_view(request, submission_id):
    submission = get_object_or_404(JobSubmission, id=submission_id, user=request.user)
    if request.method == "POST":
        company = submission.company_name
        submission.delete()
        messages.info(request, f"درخواست مربوط به «{company}» از لیست پیگیری‌ها حذف شد.")
        return redirect("submissions")
    return redirect("submissions")

