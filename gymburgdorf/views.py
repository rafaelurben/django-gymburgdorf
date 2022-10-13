from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages, auth

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

# Account

def login(request):
    return render(request, "gymburgdorf/login.html")

def logout(request):
    auth.logout(request)
    messages.success(request, "Du wurdest erfolgreich ausgeloggt!", extra_tags="alert-success")
    return redirect(reverse('gymburgdorf:home'))

# Error

def error404(request):
    return render(request, 'gymburgdorf/404.html', status=404)
