from django import forms
from django.contrib.auth.forms import User
from core.models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'job_title', 'bio', 'location', 'linkedin', 'github', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-2xl border-slate-200'}),
        }