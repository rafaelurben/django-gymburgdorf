from django.urls import path, re_path
from django.urls import include

from . import views

#######################

app_name = 'gymburgdorf'

urlpatterns = [
    # Home
    path('', views.home, name="home"),

    # Fake-Static
    path('manifest.json', views.manifest, name="manifest"),

    # account
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    # 23h
    path('23h/', include('gymburgdorf.my23h.urls')),

    # Error
    re_path('^.*$', views.error404),
]
