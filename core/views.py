from django.db.models.manager import BaseManager
from django.shortcuts import render
from core.models import Comment

# Create your views here.
def home_view(request,author_username=None):
    comments = Comment.objects.filter(status=True)
    if author_username:
        posts: BaseManager[Comment] = posts.filter(author__username = author_username)
    context = {'comments':comments}
    return render(request, "core/home.html",context)
def about_view(request):
    return render(request,'core/about.html')
def contact_view(request):
    return render(request,'core/contact.html')