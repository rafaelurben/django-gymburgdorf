from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib import auth

klassen = {
    "23h": ['lukas.beck@gymburgdorf.ch', 'david.berner@gymburgdorf.ch', 'mara.bill@gymburgdorf.ch', 'cyril.gremaud@gymburgdorf.ch', 'matthew.haldimann@gymburgdorf.ch', 'ivan.henauer@gymburgdorf.ch', 'belmin.latic@gymburgdorf.ch', 'anna.luethi@gymburgdorf.ch', 'tim.mathys@gymburgdorf.ch', 'giulia.menzi@gymburgdorf.ch',
            'vijugan.neethirajah@gymburgdorf.ch', 'elina.oppliger@gymburgdorf.ch', 'liviana.pfister@gymburgdorf.ch', 'lukas.schild@gymburgdorf.ch', 'sina.sedioli@gymburgdorf.ch', 'sanchaai.sivapalan@gymburgdorf.ch', 'abishnah.thirukkumar@gymburgdorf.ch', 'rafael.urben@gymburgdorf.ch', 'noah.wuethrich@gymburgdorf.ch']
}


def gymburgdorf_user_required(view_func=None, klasse=None):
    """
    Decorator for views that checks if the user has a @gymburgdorf.ch email connected
    Logs the user out and redirects to the error page if not.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if klasse is None:
                if request.user.social_auth.filter(provider="google-oauth2", uid__endswith="@gymburgdorf.ch").exists():
                    return view_func(request, *args, **kwargs)
                auth.logout(request)
                return redirect(reverse("gymburgdorf:error")+"?errorcode=403 Verboten&errormsg=Du musst dich mit einer @gymburgdorf.ch-Adresse anmelden, um diese Seite zu verwenden!")
            else:
                if request.user.social_auth.filter(provider="google-oauth2", uid__in=klassen[klasse]).exists():
                    return view_func(request, *args, **kwargs)
                auth.logout(request)
                return redirect(reverse("gymburgdorf:error")+f"?errorcode=403 Verboten&errormsg=Du musst Teil der Klasse {klasse.lower()}@gymburgdorf.ch sein, um diese Seite zu verwenden!")
        return _wrapped_view

    if view_func:
        return decorator(view_func)
    return decorator
