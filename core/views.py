from django.shortcuts import render


# Create your views here.
def home_view(request):
    return render(request, "core/home.html")
def about_view(request):
    return render(request,'core/about.html')
def contact_view(request):
    return render(request,'core/contact.html')