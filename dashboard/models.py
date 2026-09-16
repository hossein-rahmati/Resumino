from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    THEME_COLORS = [
        ("blue", "آبی نیلی (Blue)"),
        ("indigo", "نیلی عمیق (Indigo)"),
        ("emerald", "زمردی (Emerald)"),
        ("purple", "بنفش مدرن (Purple)"),
        ("slate", "طوسی تیره (Slate)"),
        ("amber", "کهربایی (Amber)"),
        ("rose", "سرخابی (Rose)"),
    ]

    TEMPLATES = [
        ("modern", "قالب Modern (پیش‌فرض)"),
        ("minimal", "قالب Minimal (مینیمال و تمیز)"),
        ("executive", "قالب Executive (مدیران و رهبران)"),
        ("tech_ats", "قالب Tech ATS (استاندارد نرم‌افزاری)"),
        ("creative", "قالب Creative (طراحی و خلاقیت)"),
        ("academic", "قالب Academic (آکادمیک و پژوهشی)"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes", verbose_name="کاربر")
    title = models.CharField(max_length=150, default="رزومه من", verbose_name="عنوان رزومه")
    target_job = models.CharField(max_length=150, blank=True, verbose_name="عنوان شغلی هدف")
    template_name = models.CharField(max_length=50, choices=TEMPLATES, default="modern", verbose_name="قالب انتخابی")
    theme_color = models.CharField(max_length=30, choices=THEME_COLORS, default="blue", verbose_name="رنگ تم")
    language = models.CharField(max_length=10, default="fa", choices=[("fa", "فارسی"), ("en", "English")], verbose_name="زبان رزومه")
    summary = models.TextField(blank=True, verbose_name="خلاصه درباره من")
    skills = models.CharField(max_length=300, blank=True, default="Python, Django, PostgreSQL, Git", verbose_name="مهارت‌ها (با کاما)")
    
    completion_percentage = models.PositiveIntegerField(default=75, verbose_name="درصد تکمیل")
    ats_score = models.PositiveIntegerField(default=82, verbose_name="امتیاز ATS")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    downloads_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دانلود")
    is_primary = models.BooleanField(default=False, verbose_name="رزومه اصلی")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ساخت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین بروزرسانی")

    class Meta:
        verbose_name = "رزومه"
        verbose_name_plural = "رزومه‌ها"
        ordering = ["-is_primary", "-updated_at"]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]


class JobListing(models.Model):
    JOB_TYPES = [
        ("تمام وقت", "تمام وقت"),
        ("پاره وقت", "پاره وقت"),
        ("پروژه‌ای", "پروژه‌ای"),
        ("کارآموزی", "کارآموزی"),
    ]

    WORK_MODES = [
        ("دورکاری کامل", "دورکاری کامل"),
        ("امکان دورکاری (هیبریدی)", "امکان دورکاری (هیبریدی)"),
        ("حضوری", "حضوری"),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان موقعیت شغلی")
    company_name = models.CharField(max_length=150, verbose_name="نام شرکت")
    company_initial = models.CharField(max_length=5, default="ش", verbose_name="حرف اول نام شرکت")
    company_logo_color = models.CharField(max_length=50, default="blue", verbose_name="رنگ برند لوگو")
    location = models.CharField(max_length=100, default="تهران", verbose_name="موقعیت مکانی")
    job_type = models.CharField(max_length=50, choices=JOB_TYPES, default="تمام وقت", verbose_name="نوع همکاری")
    work_mode = models.CharField(max_length=50, choices=WORK_MODES, default="امکان دورکاری (هیبریدی)", verbose_name="نحوه کار")
    salary_range = models.CharField(max_length=100, default="توافقی", verbose_name="حقوق پیشنهادی")
    experience_level = models.CharField(max_length=50, default="Senior (۳+ سال)", verbose_name="سطح ارشدیت")
    category = models.CharField(max_length=100, default="برنامه‌نویسی و نرم‌افزار", verbose_name="دسته‌بندی شغلی")
    skills_required = models.CharField(max_length=255, default="Python, Django, Docker", verbose_name="مهارت‌های مورد نیاز")
    description = models.TextField(blank=True, verbose_name="توضیحات و نیازمندی‌ها")
    benefits = models.CharField(max_length=255, blank=True, default="بیمه تکمیلی، پاداش، ساعت کاری منعطف، ناهار", verbose_name="مزایا و تسهیلات")
    
    is_featured = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")
    is_urgent = models.BooleanField(default=False, verbose_name="استخدام فوری")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")

    class Meta:
        verbose_name = "موقعیت شغلی"
        verbose_name_plural = "موقعیت‌های شغلی"
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.company_name}"

    def get_skills_list(self):
        return [s.strip() for s in self.skills_required.split(",") if s.strip()]


class JobSubmission(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار بررسی"),
        ("reviewing", "در حال بررسی"),
        ("interview", "دعوت به مصاحبه"),
        ("accepted", "پیشنهاد همکاری"),
        ("rejected", "عدم پذیرش"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", verbose_name="کاربر")
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, null=True, blank=True, related_name="applications", verbose_name="موقعیت شغلی")
    company_name = models.CharField(max_length=150, verbose_name="نام شرکت")
    job_title = models.CharField(max_length=200, verbose_name="عنوان شغل")
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications", verbose_name="رزومه ارسال‌شده")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending", verbose_name="وضعیت درخواست")
    applied_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    status_updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی وضعیت")
    note = models.TextField(blank=True, verbose_name="یادداشت کارفرما یا کاربر")
    interview_time = models.CharField(max_length=150, blank=True, verbose_name="زمان مصاحبه (در صورت تعیین)")

    class Meta:
        verbose_name = "درخواست ارسال رزومه"
        verbose_name_plural = "درخواست‌های ارسال رزومه"
        ordering = ["-applied_date"]

    def __str__(self):
        return f"{self.user.username} -> {self.job_title} ({self.company_name})"


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs", verbose_name="کاربر")
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name="saved_by", verbose_name="شغل ذخیره شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ذخیره")

    class Meta:
        verbose_name = "شغل نشان‌شده"
        verbose_name_plural = "شغل‌های نشان‌شده"
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
