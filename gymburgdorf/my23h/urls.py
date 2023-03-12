from django.urls import path, re_path

from . import views

#######################

urlpatterns = [
    # 23h home
    path('', views.home, name="23h"),

    # Maturabooks
    path('maturabooks', views.maturabooks),
    path('maturabooks/', views.maturabooks, name="23h-maturabooks"),
    path('maturabooks/api',
         views.maturabooks_api, name="23h-maturabooks-api"),

    # MULUS collection
    path('muluscollection', views.muluscollection),
    path('muluscollection/', views.muluscollection, name="23h-muluscollection"),
    path("muluscollection/api/list", views.muluscollection_api_list, name="23h-muluscollection-api-list"),
    path('muluscollection/api/action',
         views.muluscollection_api_action, name="23h-muluscollection-api-action"),

    # Not found
    re_path('^.*$', views.notfound),
]
