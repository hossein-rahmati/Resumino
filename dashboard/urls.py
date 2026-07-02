from django.urls import path
from dashboard.views import *

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path('accounts_settings/',account_settings, name="account_settings"),
    path("resume/", my_resume_view, name="my_resume"),
    path("template/", template_view, name="templates"),
    path("jobs/", jobs_view, name="jobs"),
    path('submissions/',submissions_view,name='submissions')
]
