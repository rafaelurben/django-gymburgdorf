from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .decorators import gymburgdorf_user_required
from .utils import isfloat
from .models import NotenManager, Semester, Fach, Note, Teilnote, UserContent

# Grades

# Manager


@login_required
@gymburgdorf_user_required
def api_grades_manager(request):
    if not getattr(request.user, "gymburgdorf_notenmanager", False):
        NotenManager.objects.create(user=request.user)
    return JsonResponse(request.user.gymburgdorf_notenmanager.json())

# Semester


@login_required
@gymburgdorf_user_required
@require_POST
@csrf_exempt
def api_grades_semester_add(request):
    if not getattr(request.user, "gymburgdorf_notenmanager", False):
        NotenManager.objects.create(user=request.user)
    if "title" in request.POST:
        semester = Semester.objects.create(
            manager=request.user.gymburgdorf_notenmanager, title=request.POST["title"])
        return JsonResponse({"success": True, "id": semester.pk})
    return JsonResponse({"error": "Invalid POST data!"})


@login_required
@gymburgdorf_user_required
@csrf_exempt
def api_grades_semester(request, semesterid):
    if not semesterid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Semester.objects.filter(pk=semesterid).exists():
        obj = Semester.objects.get(id=semesterid)
        if obj.manager.user == request.user:
            print(request.method)
            if request.method.lower() == "get":
                return JsonResponse(obj.json())
            if request.method.lower() == "post":
                # TODO
                return JsonResponse({"error": "Not yet implemented"})
            if request.method.lower() == "delete":
                obj.delete()
                return JsonResponse({"success": True})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Semester not found!"})

# Subject


@login_required
@gymburgdorf_user_required
@require_POST
@csrf_exempt
def api_grades_subject_add(request, semesterid):
    if not semesterid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Semester.objects.filter(pk=semesterid).exists():
        semester = Semester.objects.get(id=semesterid)
        if semester.manager.user == request.user:
            if "title" in request.POST:
                subject = Fach.objects.create(semester=semester, title=request.POST["title"], weight=float(
                    request.POST.get("weight", 1.0)))
                return JsonResponse({"success": True, "id": subject.pk})
            return JsonResponse({"error": "Invalid POST data!"})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Semester not Found!"})


@login_required
@gymburgdorf_user_required
@csrf_exempt
def api_grades_subject(request, subjectid):
    if not subjectid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Fach.objects.filter(pk=subjectid).exists():
        obj = Fach.objects.get(id=subjectid)
        if obj.semester.manager.user == request.user:
            if request.method.lower() == "get":
                return JsonResponse(obj.json())
            if request.method.lower() == "post":
                # TODO
                return JsonResponse({"error": "Not yet implemented"})
            if request.method.lower() == "delete":
                obj.delete()
                return JsonResponse({"success": True})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Not Found!"})

# Grade


@login_required
@gymburgdorf_user_required
@require_POST
@csrf_exempt
def api_grades_grade_add(request, subjectid):
    if not subjectid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Fach.objects.filter(pk=subjectid).exists():
        subject = Fach.objects.get(id=subjectid)
        if subject.semester.manager.user == request.user:
            if "title" in request.POST and "value" in request.POST and isfloat(request.POST["value"]):
                grade = Note.objects.create(
                    subject=subject, title=request.POST["title"], weight=float(request.POST.get("weight", 1.0)), value=float(request.POST["value"]), is_partial_grade=bool(request.POST.get("is_partial_grade", False)))
                return JsonResponse({"success": True, "id": grade.pk})
            return JsonResponse({"error": "Invalid POST data!"})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Subject not Found!"})


@login_required
@gymburgdorf_user_required
@csrf_exempt
def api_grades_grade(request, gradeid):
    if not gradeid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Note.objects.filter(pk=gradeid).exists():
        obj = Note.objects.get(id=gradeid)
        if obj.subject.semester.manager.user == request.user:
            if request.method.lower() == "get":
                return JsonResponse(obj.json())
            if request.method.lower() == "post":
                # TODO
                return JsonResponse({"error": "Not yet implemented"})
            if request.method.lower() == "delete":
                obj.delete()
                return JsonResponse({"success": True})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Not Found!"})

# Partial grade


@login_required
@gymburgdorf_user_required
@require_POST
@csrf_exempt
def api_grades_partialgrade_add(request, gradeid):
    if not gradeid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Note.objects.filter(pk=gradeid).exists():
        grade = Note.objects.get(id=gradeid)
        if grade.subject.semester.manager.user == request.user:
            if "title" in request.POST and "value" in request.POST and isfloat(request.POST["value"]):
                partialgrade = Teilnote.objects.create(
                    grade=grade, title=request.POST["title"], weight=float(request.POST.get("weight", 1.0)), value=float(request.POST["value"]))
                return JsonResponse({"success": True, "id": partialgrade.pk})
            return JsonResponse({"error": "Invalid POST data!"})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Subject not Found!"})


@login_required
@gymburgdorf_user_required
@csrf_exempt
def api_grades_partialgrade(request, partialgradeid):
    if not partialgradeid.isdigit():
        return JsonResponse({"error": "Not an integer!"})
    if Teilnote.objects.filter(pk=partialgradeid).exists():
        obj = Teilnote.objects.get(id=partialgradeid)
        if obj.grade.subject.semester.manager.user == request.user:
            if request.method.lower() == "get":
                return JsonResponse(obj.json())
            if request.method.lower() == "post":
                # TODO
                return JsonResponse({"error": "Not yet implemented"})
            if request.method.lower() == "delete":
                obj.delete()
                return JsonResponse({"success": True})
        return JsonResponse({"error": "No permission!"})
    return JsonResponse({"error": "Not Found!"})

# UserContent


@login_required
@gymburgdorf_user_required
@csrf_exempt
def api_usercontent_list(request):
    data = {
        "objects": [
            q.json(request=request) for q in UserContent.objects.filter(published=True).order_by('published_at')
        ],
        "myobjects": [
            q.json(request=request) for q in UserContent.objects.filter(user=request.user).order_by('published', 'published_at')
        ]
    }
    if request.user.has_perm("gymburgdorf.change_usercontent"):
        data["verifyqueue"] = [
            q.json(request=request) for q in UserContent.objects.filter(published=False)
        ]
    return JsonResponse(data)


@login_required
@gymburgdorf_user_required
@require_POST
@csrf_exempt
def api_usercontent_suggest(request):
    try:
        kategorie = request.POST.get("kategorie")
        if not kategorie in map(lambda x: x[0], UserContent.KATEGORIEN):
            return JsonResponse({
                "error": "invalid-category",
            }, status=400)
        obj = UserContent.objects.create(
            titel=request.POST.get('titel'),
            beschreibung=request.POST.get('beschreibung'),
            personen=request.POST.get('personen'),
            kategorie=kategorie,
            user=request.user,
            published=request.user.has_perm('gymburgdorf.publish_usercontent'),
        )
        return JsonResponse({
            "success": True,
            "obj": obj.json(),
        })
    except (AttributeError, ValidationError):
        return JsonResponse({
            "error": "invalid-data",
        }, status=400)


@login_required
@gymburgdorf_user_required
@permission_required("gymburgdorf.publish_usercontent")
@require_POST
@csrf_exempt
def api_usercontent_publish(request):
    pid = request.POST.get('id', None)
    if UserContent.objects.filter(id=pid).exists():
        obj = UserContent.objects.get(id=pid)
        obj.published = True
        obj.save()
        return JsonResponse({
            "success": True,
        }, status=200)
    return JsonResponse({
        "error": "object-not-found",
    }, status=404)


@login_required
@gymburgdorf_user_required
@require_POST
@csrf_exempt
def api_usercontent_delete(request):
    pid = request.POST.get('id', None)
    if UserContent.objects.filter(id=pid).exists():
        obj = UserContent.objects.get(id=pid)
        if request.user.has_perm('gymburgdorf.delete_usercontent') or (request.user == obj.user and not obj.published):
            obj.delete()
            return JsonResponse({
                "success": True,
            }, status=200)
        return JsonResponse({
            "error": "no-permission",
        }, status=403)
    return JsonResponse({
        "error": "object-not-found",
    }, status=404)
