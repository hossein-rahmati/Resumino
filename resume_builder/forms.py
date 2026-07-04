from django import forms
from core.models import Resume, Submission , Comment

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'job_title', 'location', 'bio',
            'linkedin', 'github', 'website',
            'experience', 'education', 'skills',
            'projects', 'certificates',
            'template_name', 'is_public'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'job_title': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'linkedin': forms.URLInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'github': forms.URLInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'experience': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm font-mono focus:ring-2 focus:ring-blue-500', 'placeholder': 'JSON array of experiences'}),
            'education': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm font-mono focus:ring-2 focus:ring-blue-500', 'placeholder': 'JSON array of educations'}),
            'skills': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm font-mono focus:ring-2 focus:ring-blue-500', 'placeholder': '["Python", "Django"]'}),
            'projects': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm font-mono focus:ring-2 focus:ring-blue-500', 'placeholder': 'JSON array of projects'}),
            'certificates': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm font-mono focus:ring-2 focus:ring-blue-500', 'placeholder': 'JSON array of certificates'}),
            'template_name': forms.Select(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['resume', 'company_name', 'job_title', 'job_url', 'status', 'notes']
        widgets = {
            'resume': forms.Select(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'job_title': forms.TextInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'job_url': forms.URLInput(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'status': forms.Select(attrs={'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-5 py-3.5 bg-gray-50/80 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'نظر خود را بنویسید...'
            }),
        }