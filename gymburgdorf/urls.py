from django.urls import path, re_path
from django.urls import include

from . import views, views_api as apiviews

#######################

app_name = 'gymburgdorf'

urlpatterns = [
    # Home
    path('', views.main, name="main"),

    # Seiten
    path('home', views.home, name="home"),
    path('infoboard', views.infoboard, name="infoboard"),
    path('kalender', views.kalender, name="kalender"),
    path('kalender2', views.kalender2, name="kalender2"),
    path('merch', views.merch, name="merch"),
    path('noten', views.noten, name="noten"),
    path('stundenplan', views.stundenplan, name="stundenplan"),
    path('usercontent', views.usercontent, name="usercontent"),

    # API
    path('api/grades/',
         apiviews.api_grades_manager, name="api-grades-manager"),
    path('api/grades/semester/add',
         apiviews.api_grades_semester_add, name="api-grades-semester-add"),
    path('api/grades/semester/<semesterid>',
         apiviews.api_grades_semester, name="api-grades-semester"),
    path('api/grades/subject/add/<semesterid>',
         apiviews.api_grades_subject_add, name="api-grades-subject-add"),
    path('api/grades/subject/<subjectid>',
         apiviews.api_grades_subject, name="api-grades-subject"),
    path('api/grades/grade/add/<subjectid>',
         apiviews.api_grades_grade_add, name="api-grades-grade-add"),
    path('api/grades/grade/<gradeid>',
         apiviews.api_grades_grade, name="api-grades-grade"),
    path('api/grades/partialgrade/add/<gradeid>',
         apiviews.api_grades_partialgrade_add, name="api-grades-grade-add"),
    path('api/grades/partialgrade/<partialgradeid>',
         apiviews.api_grades_partialgrade, name="api-grades-grade"),

    path('api/usercontent/',
         apiviews.api_usercontent_list, name="api-usercontent-list"),
    path('api/usercontent/suggest',
         apiviews.api_usercontent_suggest, name="api-usercontent-suggest"),
    path('api/usercontent/publish',
         apiviews.api_usercontent_publish, name="api-usercontent-publish"),
    path('api/usercontent/delete',
         apiviews.api_usercontent_delete, name="api-usercontent-delete"),


    # Fake-Static
    path('manifest.webmanifest', views.manifest, name="manifest"),
    path('service-worker.js', views.service_worker, name="service-worker"),

    # Account
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    # 23h
    path('23h/', include('gymburgdorf.my23h.urls')),

    # Error
    path('error', views.error, name="error"),
    re_path('^.*$', views.error),
]
