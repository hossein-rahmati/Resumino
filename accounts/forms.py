import re
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

INPUT_CSS = "w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none transition-all duration-300 focus:bg-white focus:border-blue-600 focus:ring-4 focus:ring-blue-500/10 text-sm"
CHECKBOX_CSS = "w-4 h-4 text-blue-600 bg-slate-100 border-slate-300 rounded focus:ring-blue-500 focus:ring-2"


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام",
        widget=forms.TextInput(attrs={"placeholder": "مثال: علی", "class": INPUT_CSS}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={"placeholder": "مثال: محمدی", "class": INPUT_CSS}),
    )
    email = forms.EmailField(
        required=True,
        label="آدرس ایمیل",
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com", "class": INPUT_CSS}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "نام کاربری"
        self.fields["username"].widget.attrs.update({
            "placeholder": "مثال: ali_99 (فقط حروف، اعداد و _)",
            "class": INPUT_CSS,
        })
        self.fields["username"].help_text = "می‌تواند شامل حروف انگلیسی، اعداد و زیرخط باشد."

        if "password1" in self.fields:
            self.fields["password1"].label = "رمز عبور"
            self.fields["password1"].widget.attrs.update({
                "placeholder": "حداقل ۸ کاراکتر ترکیبی",
                "class": INPUT_CSS,
            })
            self.fields["password1"].help_text = ""

        if "password2" in self.fields:
            self.fields["password2"].label = "تکرار رمز عبور"
            self.fields["password2"].widget.attrs.update({
                "placeholder": "رمز عبور را مجدداً وارد کنید",
                "class": INPUT_CSS,
            })
            self.fields["password2"].help_text = ""

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if not re.match(r"^[\w.@+-]+$", username):
            raise ValidationError("نام کاربری تنها می‌تواند شامل حروف انگلیسی، اعداد و @/./+/-/_ باشد.")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("این نام کاربری قبلاً ثبت شده است. لطفاً نام کاربری دیگری انتخاب کنید.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("کاربری با این ایمیل قبلاً ثبت‌نام کرده است.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="نام کاربری یا ایمیل",
        widget=forms.TextInput(attrs={
            "placeholder": "نام کاربری یا ایمیل خود را وارد کنید",
            "class": INPUT_CSS,
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "رمز عبور خود را وارد کنید",
            "class": INPUT_CSS,
        }),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label="مرا به خاطر بسپار",
        widget=forms.CheckboxInput(attrs={"class": CHECKBOX_CSS}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["invalid_login"] = "نام کاربری (یا ایمیل) یا رمز عبور اشتباه است."
        self.error_messages["inactive"] = "این حساب کاربری غیرفعال شده است."


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "نام"
        self.fields["first_name"].widget.attrs.update({"class": INPUT_CSS})
        self.fields["last_name"].label = "نام خانوادگی"
        self.fields["last_name"].widget.attrs.update({"class": INPUT_CSS})
        self.fields["email"].label = "آدرس ایمیل"
        self.fields["email"].widget.attrs.update({"class": INPUT_CSS})

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("این ایمیل توسط کاربر دیگری استفاده شده است.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("headline", "phone_number", "bio", "avatar")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "class": INPUT_CSS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "avatar":
                field.widget.attrs.update({"class": INPUT_CSS})
            else:
                field.widget.attrs.update({
                    "class": "block w-full text-sm text-slate-500 file:mr-0 file:ml-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
                })


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "رمز عبور فعلی"
        self.fields["new_password1"].label = "رمز عبور جدید"
        self.fields["new_password2"].label = "تکرار رمز عبور جدید"

        for field in self.fields.values():
            field.widget.attrs.update({"class": INPUT_CSS})
            field.help_text = ""


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="آدرس ایمیل حساب کاربری",
        widget=forms.EmailInput(attrs={
            "placeholder": "ایمیلی که با آن ثبت‌نام کرده‌اید را وارد کنید",
            "class": INPUT_CSS,
            "autofocus": True,
        }),
    )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].label = "رمز عبور جدید"
        self.fields["new_password2"].label = "تکرار رمز عبور جدید"

        for field in self.fields.values():
            field.widget.attrs.update({"class": INPUT_CSS})
            field.help_text = ""

