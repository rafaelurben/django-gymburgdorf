from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import mark_safe
from django.conf import settings

import requests
import datetime


def htmlurl(url, external=False, text="Bearbeiten"):
    return mark_safe(f'<a target="_blank" href="{url}">{text}</a>') if external else mark_safe(f'<a href="{url}">{text}</a>')


def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def durchschnitt(wertgewichtpaare: list):
    if wertgewichtpaare:
        gesamtnote = 0
        gesamtgewicht = 0
        for note, gewicht in wertgewichtpaare:
            if note and gewicht:
                gesamtnote += note*gewicht
                gesamtgewicht += gewicht
        if gesamtgewicht > 0 and gesamtnote > 0:
            return round(gesamtnote / gesamtgewicht, 3)
    return None

def get_access_token(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    token = social.extra_data['access_token']
    return token


def get_calender():
    url = "https://content.googleapis.com/calendar/v3/calendars/kalender@gymburgdorf.ch/events"
    r = requests.get(url, params={
        "oderBy": "startTime",
        "singleEvents": True,
        "timeMin": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "key": settings.GOOGLE_API_KEY,
    })
    j = r.json()
    try:
        items = [
            {
                # "id": item["id"],
                "summary": item["summary"],
                "url": item["htmlLink"],
                "creator": item["creator"],
                "organizer": item["organizer"],
                "start": item["start"]["dateTime"] if "dateTime" in item["start"] else item["start"]["date"],
                "end": item["end"]["dateTime"] if "dateTime" in item["end"] else item["end"]["date"],
            } for item in j["items"]
        ]

        data = {
            "description": j["description"],
            "summary": j["summary"],
            "updated": j["updated"],
            "currentTime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "items": sorted(items, key=lambda k: k['start']),
        }
        return data
    except KeyError as e:
        print(e)
        return j
