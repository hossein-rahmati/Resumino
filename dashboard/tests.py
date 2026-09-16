from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Resume, JobListing, JobSubmission, SavedJob


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123!",
            first_name="حسین",
            last_name="رحمتی",
        )
        self.client.login(username="testuser", password="StrongPassword123!")

    def test_dashboard_overview_authenticated(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")
        self.assertContains(response, "داشبورد اصلی")
        self.assertContains(response, "حسین")

    def test_my_resumes_view(self):
        response = self.client.get(reverse("my_resume"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/my_resume.html")
        self.assertContains(response, "رزومه‌های من")

    def test_create_resume(self):
        response = self.client.post(
            reverse("create_resume"),
            {
                "title": "رزومه بک‌اند پایتون",
                "target_job": "Senior Python Developer",
                "template_name": "tech_ats",
                "language": "fa",
                "skills": "Python, Django, Celery",
                "summary": "توسعه‌دهنده با ۵ سال تجربه کار با پایتون و جنگو",
                "is_primary": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resume.objects.filter(user=self.user, title="رزومه بک‌اند پایتون").exists())

    def test_edit_resume(self):
        resume = Resume.objects.create(
            user=self.user,
            title="رزومه قدیمی",
            target_job="Junior Dev",
        )
        response = self.client.post(
            reverse("edit_resume", args=[resume.id]),
            {
                "title": "رزومه جدید و بروز",
                "target_job": "Senior Dev",
                "template_name": "minimal",
                "language": "fa",
                "skills": "Python, Django",
                "summary": "توضیحات بروزرسانی شده",
            },
        )
        self.assertEqual(response.status_code, 302)
        resume.refresh_from_db()
        self.assertEqual(resume.title, "رزومه جدید و بروز")
        self.assertEqual(resume.target_job, "Senior Dev")

    def test_delete_resume(self):
        resume = Resume.objects.create(
            user=self.user,
            title="رزومه موقت جهت حذف",
        )
        response = self.client.post(reverse("delete_resume", args=[resume.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Resume.objects.filter(id=resume.id).exists())

    def test_templates_gallery_view(self):
        response = self.client.get(reverse("template"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/template.html")
        self.assertContains(response, "Modern")
        self.assertContains(response, "Minimal")
        self.assertContains(response, "Tech ATS")

    def test_jobs_view(self):
        response = self.client.get(reverse("jobs"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/jobs.html")
        self.assertContains(response, "فرصت‌های شغلی")

    def test_apply_job(self):
        job = JobListing.objects.create(
            title="Django Developer",
            company_name="دیجی‌کالا",
            company_initial="د",
        )
        resume = Resume.objects.create(
            user=self.user,
            title="رزومه ارسال",
            is_primary=True,
        )
        response = self.client.post(
            reverse("apply_job", args=[job.id]),
            {"resume_id": resume.id, "note": "علاقه‌مند به همکاری"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobSubmission.objects.filter(user=self.user, job=job).exists())

    def test_submissions_view(self):
        response = self.client.get(reverse("submissions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/submissions.html")
        self.assertContains(response, "پیگیری درخواست‌های ارسالی")

    def test_add_manual_submission(self):
        response = self.client.post(
            reverse("add_manual_submission"),
            {
                "company_name": "Google",
                "job_title": "Software Engineer",
                "status": "interview",
                "note": "مصاحبه تلفنی اولیه انجام شد",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobSubmission.objects.filter(user=self.user, company_name="Google").exists())

