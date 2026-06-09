from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

INPUT_CSS = "w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "نام کاربری"
        self.fields['username'].widget.attrs.update({'placeholder': 'مثال: ali_99'})
        self.fields['email'].label = "آدرس ایمیل"
        self.fields['email'].widget.attrs.update({'placeholder': 'example@mail.com'})
        self.fields['password1'].label = "کلمه عبور"
        self.fields['password1'].widget.attrs.update({'placeholder': 'یک کلمه عبور انتخاب کنید'})
        self.fields['password2'].label = "کلمه عبور را تایید کنید"
        self.fields['password2'].widget.attrs.update({'placeholder': 'کلمه عبور را تکرار کنید'})

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": INPUT_CSS})
            field.widget.attrs.setdefault("placeholder", field.label)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری"
        self.fields['username'].widget.attrs.update({'placeholder': 'نام کاربری خود را وارد کنید'})
        self.fields['password'].label = "کلمه عبور"
        self.fields['password'].widget.attrs.update({'placeholder': 'کلمه عبور خود را وارد کنید'})

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": INPUT_CSS})
            field.widget.attrs.setdefault("placeholder", field.label)
