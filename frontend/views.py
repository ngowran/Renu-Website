from django.shortcuts import render

# Create your views here.

def index(request, *args, **kwargs):
  return render(request, 'frontend/index.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")