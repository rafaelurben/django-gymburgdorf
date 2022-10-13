from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib import auth, messages

klassen = {
    "23h": ['lukas.beck@gymburgdorf.ch', 'david.berner@gymburgdorf.ch', 'mara.bill@gymburgdorf.ch', 'cyril.gremaud@gymburgdorf.ch', 'matthew.haldimann@gymburgdorf.ch', 'ivan.henauer@gymburgdorf.ch', 'belmin.latic@gymburgdorf.ch', 'anna.luethi@gymburgdorf.ch', 'tim.mathys@gymburgdorf.ch', 'giulia.menzi@gymburgdorf.ch',
            'vijugan.neethirajah@gymburgdorf.ch', 'elina.oppliger@gymburgdorf.ch', 'liviana.pfister@gymburgdorf.ch', 'lukas.schild@gymburgdorf.ch', 'sina.sedioli@gymburgdorf.ch', 'sanchaai.sivapalan@gymburgdorf.ch', 'abishnah.thirukkumar@gymburgdorf.ch', 'rafael.urben@gymburgdorf.ch', 'noah.wuethrich@gymburgdorf.ch']
}

teachers = ['adrian.luethi@gymburgdorf.ch']

def gymburgdorf_user_required(view_func=None, klasse=None, additional_emails=teachers):
    """
    Decorator for views that checks if the user has a @gymburgdorf.ch email connected
    Logs the user out and redirects to the error page if not.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.social_auth.filter(provider="google-oauth2", uid__endswith="@gymburgdorf.ch").exists():
                auth.logout(request)
                messages.error(request, "Du musst dich mit einer @gymburgdorf.ch-Adresse anmelden, um diese Seite zu verwenden!", extra_tags="alert-danger")
                messages.warning(request, "Du wurdest ausgeloggt!", extra_tags="alert-warning")
                return redirect(reverse('gymburgdorf:home'))

            if klasse is not None:
                if not request.user.social_auth.filter(provider="google-oauth2", uid__in=klassen[klasse]).exists():
                    if not (additional_emails and request.user.social_auth.filter(provider="google-oauth2", uid__in=additional_emails).exists()):
                        messages.error(request, f"Du musst Teil der Klasse {klasse.lower()}@gymburgdorf.ch sein, um diese Seite zu verwenden!", extra_tags="alert-danger")
                        return redirect(reverse("gymburgdorf:home"))
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if view_func:
        return decorator(view_func)
    return decorator
