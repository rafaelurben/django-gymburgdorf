from django.urls import path, re_path

from . import views

#######################

urlpatterns = [
    # 23h home
    path('', views.home, name="23h"),

    # 23h account
    path('login', views.login, name="23h-login"),
    path('logout', views.logout, name="23h-logout"),

    # Maturabooks
    path('maturabooks', views.maturabooks),
    path('maturabooks/', views.maturabooks, name="23h-maturabooks"),
    path('maturabooks/api',
         views.maturabooks_api, name="23h-maturabooks-api"),

    # MULUS collection
    path('muluscollection', views.muluscollection),
    path('muluscollection/', views.muluscollection, name="23h-muluscollection"),
    path('muluscollection/api',
         views.muluscollection_api, name="23h-muluscollection-api"),

    # Not found
    re_path('^.*$', views.notfound),
]