from django.shortcuts import render
from django.urls import reverse

# Create your views here.

# Home

def home(request):
    return render(request, "gymburgdorf/home.html")

# Fake-Static

def manifest(request):
    response = render(request, "gymburgdorf/manifest.json", {})
    response['Content-Type'] = 'text/json'
    response["Service-Worker-Allowed"] = reverse('gymburgdorf:home')
    return response

# Error

def error404(request):
    return render(request, 'gymburgdorf/404.html')
