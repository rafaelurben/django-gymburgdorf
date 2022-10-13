from django.conf import settings

import requests
import datetime

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
