from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse

from .utils import get_access_token, get_calender
from .models import Info, UserContent
from .decorators import gymburgdorf_user_required

# Create your views here.

# Account

def login(request):
    return render(request, "gymburgdorf/login.html")

def logout(request):
    auth.logout(request)
    return redirect(reverse('gymburgdorf:login'))

# Main


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def main(request):
    return render(request, "gymburgdorf/main.html")

# Seiten


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def home(request):
    return render(request, "gymburgdorf/pages/home.html", {
        "infos": Info.objects.filter(hidden=False),
    })


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def infoboard(request):
    return render(request, "gymburgdorf/pages/infoboard.html")


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def kalender(request):
    return render(request, "gymburgdorf/pages/kalender_embed.html")


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def kalender2(request):
    # return render(request, "gymburgdorf/pages/kalender.html", {"kalender": get_calender()})
    return JsonResponse(get_calender())


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def noten(request):
    return render(request, "gymburgdorf/pages/noten.html")


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def stundenplan(request):
    return render(request, "gymburgdorf/pages/stundenplan.html")


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def usercontent(request):
    return render(request, "gymburgdorf/pages/usercontent.html", {
        "usercontentcategories": dict(UserContent.KATEGORIEN),
    })

# Versteckte Seiten


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required
def merch(request):
    return render(request, "gymburgdorf/pages/merch.html")

# Fake-Static


def manifest(request):
    response = render(request, "gymburgdorf/manifest.webmanifest", {})
    response['Content-Type'] = 'text/json'
    response["Service-Worker-Allowed"] = "/"
    return response


def service_worker(request):
    response = render(request, "gymburgdorf/service-worker.js", {})
    response['Content-Type'] = 'text/javascript'
    response["Service-Worker-Allowed"] = "/"
    return response


# Error

def error(request):
    return render(request, 'gymburgdorf/error.html', {
        "errorcode": request.GET.get("errorcode") or "Error 404",
        "errormsg": request.GET.get("errormsg") or "Diese Seite wurde nicht gefunden!"
    })
