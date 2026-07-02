from django.urls import path
from dashboard.views import *

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path('accounts_settings/',account_settings, name="account_settings"),
    path("resume/", my_resume_view, name="my_resume"),
    path("template/", template_view, name="template"),
    path("jobs/", jobs_view, name="job"),
    path('submissions/',submissions_view,name='submissions')
]
