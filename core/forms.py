from django import forms
from django.contrib.auth.models import User
from core.models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'job_title', 'bio', 'location', 'linkedin', 'github', 'website']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'job_title': forms.TextInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'location': forms.TextInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'linkedin': forms.URLInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'github': forms.URLInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'website': forms.URLInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white focus:border-blue-500 transition'}),
            'avatar': forms.FileInput(attrs={'class': 'w-full rounded-2xl border-slate-200 p-3 bg-slate-50 focus:bg-white'}),
        }