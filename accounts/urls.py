from django.urls import path
from .views import (
    register_view,
    CustomLoginView,
    custom_logout_view,
    dashboard_view,
    profile_settings_view,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", custom_logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("settings/", profile_settings_view, name="profile_settings"),
    path("password-change/", CustomPasswordChangeView.as_view(), name="password_change"),
    # Password Reset
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
