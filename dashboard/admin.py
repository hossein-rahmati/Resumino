from django.contrib import admin
from .models import Resume, JobListing, JobSubmission, SavedJob


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "template_name", "theme_color", "completion_percentage", "ats_score", "is_primary", "updated_at")
    list_filter = ("template_name", "theme_color", "is_primary", "language")
    search_fields = ("title", "user__username", "user__first_name", "user__last_name", "target_job")


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "location", "job_type", "work_mode", "salary_range", "is_featured", "is_urgent", "created_at")
    list_filter = ("job_type", "work_mode", "is_featured", "is_urgent", "category")
    search_fields = ("title", "company_name", "skills_required", "location")


@admin.register(JobSubmission)
class JobSubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "company_name", "status", "resume", "applied_date")
    list_filter = ("status", "applied_date")
    search_fields = ("user__username", "job_title", "company_name", "note")


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "created_at")
    search_fields = ("user__username", "job__title", "job__company_name")

