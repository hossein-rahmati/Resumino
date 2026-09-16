from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure profile exists
            Profile.objects.get_or_create(user=user)
            # Log the user in directly after registration
            login(request, user, backend="accounts.backends.EmailOrUsernameBackend")
            messages.success(request, f"خوش آمدید، {user.get_full_name() or user.username}! حساب کاربری شما با موفقیت ساخته شد.")
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me", True)
        if not remember_me:
            # Session expires on browser close
            self.request.session.set_expiry(0)
        else:
            # Default 2 weeks (1209600s)
            self.request.session.set_expiry(1209600)

        response = super().form_valid(form)
        user = self.request.user
        display_name = user.get_full_name().strip() or user.username
        messages.success(self.request, f"خوش آمدید، {display_name}!")
        return response


@require_POST
def custom_logout_view(request):
    logout(request)
    messages.info(request, "با موفقیت از حساب کاربری خود خارج شدید.")
    return redirect("core:home")


@login_required
def dashboard_view(request):
    return redirect("dashboard")


@login_required
def profile_settings_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "اطلاعات پروفایل شما با موفقیت بروزرسانی شد.")
            return redirect("profile_settings")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/profile_settings.html",
        {"u_form": u_form, "p_form": p_form, "profile": profile},
    )


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("profile_settings")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "رمز عبور شما با موفقیت تغییر کرد.")
        return response


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = CustomPasswordResetForm
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"

