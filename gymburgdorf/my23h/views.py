from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.http import JsonResponse

from .models import MaturaBookSelection, MulusCollectionPerson, MulusCollectionQuote, MulusCollectionQuoteReview
from ..decorators import gymburgdorf_user_required

# Home

@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required(klasse="23h")
def home(request):
    return render(request, "gymburgdorf/23h/home.html")

def notfound(request):
    messages.error(request, "Diese Seite existiert nicht!", extra_tags="alert-danger")
    return render(request, "gymburgdorf/404.html")

# Maturabooks

@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required(klasse="23h")
def maturabooks(request):
    return render(request, "gymburgdorf/23h/maturabooks.html", {
        "can_reserve": MaturaBookSelection.is_reservation_possible_for_user(request.user),
        "reservations": MaturaBookSelection.getselectionsforuser(request.user, typ="reserved"),
        "presaves": MaturaBookSelection.getselectionsforuser(request.user, typ="presaved"),
        "booklist": MaturaBookSelection.getuserbooklist(request.user),
    })


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required(klasse="23h")
def maturabooks_api(request):
    try:
        book = request.GET.get("book", request.GET.get("b"))
        book = strip_tags(book)
        action = request.GET.get("action", request.GET.get("a"))
    except KeyError:
        messages.error(request, "Ungültige Anfrage!", extra_tags="alert-danger")
        return redirect(reverse("gymburgdorf:23h-maturabooks"))

    userselection = MaturaBookSelection.objects.filter(user=request.user, book=book, is_removed=False)
    usersel_res = MaturaBookSelection.objects.filter(user=request.user, book=book, is_removed=False).filter(typ="reserved").first()
    usersel_pre = MaturaBookSelection.objects.filter(user=request.user, book=book, is_removed=False).filter(typ="presaved").first()

    if action == "reserve":
        if usersel_res is None:
            if MaturaBookSelection.is_reservation_possible_for_book(book):
                if MaturaBookSelection.is_reservation_possible_for_user(request.user):
                    MaturaBookSelection.objects.create(user=request.user, book=book, typ="reserved")

                    if usersel_pre is not None:
                        usersel_pre.softremove()
                        messages.success(request, f"Du hast '{book}' reserviert. Es ist nun nicht mehr auf deiner 'vorgemerkt' Liste.", extra_tags="alert-success")
                    else:
                        messages.success(request, f"Du hast '{book}' reserviert.", extra_tags="alert-success")
                else:
                    messages.error(request, f"Du kannst nicht mehr als {MaturaBookSelection.MAX_RESERVATIONS_PER_USER} Bücher reservieren.", extra_tags="alert-danger")
            else:
                messages.error(request, f"'{book}' hat bereits zu viele Reservationen.", extra_tags="alert-danger")
        else:
            messages.warning(request, f"Du hast '{book}' bereits reserviert.", extra_tags="alert-warning")
    elif action == "presave":
        if usersel_pre is None:
            MaturaBookSelection.objects.create(user=request.user, book=book, typ="presaved")

            if usersel_res is not None:
                usersel_res.softremove()
                messages.success(request, f"Du hast die Reservation für '{book}' aufgehoben und es auf die 'vorgemerkt' Liste gesetzt.", extra_tags="alert-success")
            else:
                messages.success(request, f"Du hast '{book}' vorgemerkt.", extra_tags="alert-success")
        else:
            messages.warning(request, f"Du hast '{book}' bereits vorgemerkt.", extra_tags="alert-warning")
    elif action == "remove":
        if userselection.exists():
            userselection.update(is_removed=True)
            messages.success(request, f"Du hast '{book}' von deiner Liste entfernt.", extra_tags="alert-success")
        else:
            messages.error(request, f"Das Buch '{book}' ist gar nicht auf deiner Liste.", extra_tags="alert-warning")
    else:
        messages.error(request, f"Ungültige Aktions: '{action}'!", extra_tags="alert-danger")
    return redirect(reverse('gymburgdorf:23h-maturabooks'))

# MULUS collection


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required(klasse="23h")
def muluscollection(request):
    all_people = MulusCollectionPerson.objects.all().order_by('first_name', 'last_name')
    if request.method == "POST":
        try:        
            content = request.POST.get("content")
            content = strip_tags(content)
            people_raw = request.POST.getlist("people")
            people = map(lambda pid: MulusCollectionPerson.objects.get(id=pid), people_raw)

            new = MulusCollectionQuote.objects.create(content=content, created_by=request.user)
            new.people.set(people)
            messages.success(request, "Das Zitat wurde erfolgreich erstellt!", extra_tags="alert-success")
        except (KeyError, ValueError, MulusCollectionPerson.DoesNotExist):
            messages.error(request, "Ungültige Anfrage!", extra_tags="alert-danger")
        return redirect(reverse("gymburgdorf:23h-muluscollection"))
    else:
        quotes = MulusCollectionQuote.get_quotes_with_reviews(request.user)
        return render(request, "gymburgdorf/23h/muluscollection.html", {
            "people": all_people,
            "quotes": quotes,
        })


@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required(klasse="23h")
def muluscollection_api_list(request):
    query = request.GET.get("q") or ""
    try:
        people_query = request.GET.get("p").split(',') or []
        people_query = list(map(int, people_query))
        people_query = MulusCollectionPerson.objects.filter(id__in=people_query)
    except (KeyError, ValueError, MulusCollectionPerson.DoesNotExist):
        people_query = []

    quotes = MulusCollectionQuote.get_quotes_with_reviews(request.user).filter(content__icontains=query)

    if people_query:
        print(people_query)
        new_quotes = []

        for quote in quotes:
            has_all_people = True
            for person in people_query:
                if not person in quote.people.all():
                    has_all_people = False
                    break
            
            if has_all_people:
                new_quotes.append(quote)

        quotes = new_quotes
    return JsonResponse({
        "quotes": [quote.as_dict(request.user) for quote in quotes],
    })

@login_required(login_url=reverse_lazy("gymburgdorf:login"))
@gymburgdorf_user_required(klasse="23h")
def muluscollection_api_action(request):
    try:
        quoteid = request.GET.get("quote", request.GET.get("q"))
        action = request.GET.get("action", request.GET.get("a"))
    except KeyError:
        # messages.error(request, "Ungültige Anfrage!", extra_tags="alert-danger")
        return JsonResponse({"success": False, "message": "Ungültige Anfrage!"})

    if not MulusCollectionQuote.objects.filter(id=quoteid).exists():
        # messages.error(request, "Zitat wurde nicht gefunden!", extra_tags="alert-danger")
        return JsonResponse({"success": False, "message": "Zitat wurde nicht gefunden!"})
    quote = MulusCollectionQuote.objects.get(id=quoteid)

    if action == "delete":
        if quote.created_by == request.user or request.user.is_superuser:
            quote.delete()
            # messages.success(request, "Das Zitat wurde erfolgreich gelöscht!", extra_tags="alert-success")
            return JsonResponse({"success": True, "quote_id": quoteid, "deleted": True, "message": "Das Zitat wurde erfolgreich gelöscht!"})
        else:
            # messages.error(request, "Du hast dazu keine Berechtigung!", extra_tags="alert-danger")
            return JsonResponse({"success": False, "quote_id": quoteid, "message": "Du hast dazu keine Berechtigung!"})
    elif action == "remove_review":
        if quote.reviews.filter(user=request.user).exists():
            quote.reviews.filter(user=request.user).delete()
            # messages.success(request, "Deine Bewertung wurde erfolgreich entfernt!", extra_tags="alert-success")
            return JsonResponse({"success": True, "quote": quote.as_dict(request.user), "message": "Deine Bewertung wurde erfolgreich entfernt!"})
        else:
            # messages.error(request, "Du hast das Zitat noch gar nicht bewertet!", extra_tags="alert-warning")
            return JsonResponse({"success": False, "quote": quote.as_dict(request.user), "message": "Du hast das Zitat noch gar nicht bewertet!"})
    elif action == "like":
        if quote.reviews.filter(user=request.user).exists():
            review = quote.reviews.get(user=request.user)
            if not review.like:
                review.like = True
                review.save()
                # messages.success(request, "Deine Bewertung wurde zu gefällt mir geändert!", extra_tags="alert-success")
                return JsonResponse({"success": True, "quote": quote.as_dict(request.user), "message": "Deine Bewertung wurde zu gefällt mir geändert!"})
            else:
                # messages.warning(request, "Du hast das Zitat bereits mit gefällt mir markiert!", extra_tags="alert-warning")
                return JsonResponse({"success": None, "quote": quote.as_dict(request.user), "message": "Du hast das Zitat bereits mit gefällt mir markiert!"})
        else:
            quote.reviews.create(user=request.user, like=True)
            # messages.success(request, "Das Zitat wurde erfolgreich mit gefällt mir markiert!", extra_tags="alert-success")
            return JsonResponse({"success": True, "quote": quote.as_dict(request.user), "message": "Das Zitat wurde erfolgreich mit gefällt mir markiert!"})
    elif action == "dislike":
        if quote.reviews.filter(user=request.user).exists():
            review = quote.reviews.get(user=request.user)
            if review.like:
                review.like = False
                review.save()
                # messages.success(request, "Deine Bewertung wurde zu gefällt mir nicht geändert!", extra_tags="alert-success")
                return JsonResponse({"success": True, "quote": quote.as_dict(request.user), "message": "Deine Bewertung wurde zu gefällt mir nicht geändert!"})
            else:
                # messages.warning(request, "Du hast das Zitat bereits mit gefällt mir nicht markiert!", extra_tags="alert-warning")
                return JsonResponse({"success": None, "quote": quote.as_dict(request.user), "message": "Du hast das Zitat bereits mit gefällt mir nicht markiert!"})
        else:
            quote.reviews.create(user=request.user, like=False)
            # messages.success(request, "Das Zitat wurde erfolgreich mit gefällt mir nicht markiert!", extra_tags="alert-success")
            return JsonResponse({"success": True, "quote": quote.as_dict(request.user), "message": "Das Zitat wurde erfolgreich mit gefällt mir nicht markiert!"})
    else:
        # messages.error(request, f"Ungültige Aktions: '{action}'!", extra_tags="alert-danger")
        return JsonResponse({"success": False, "quote": quote.as_dict(request.user), "message": f"Ungültige Aktions: '{action}'!"})
    # return redirect(reverse('gymburgdorf:23h-muluscollection'))

# Summaries

def summaries(request):
    return render(request, "gymburgdorf/23h/summaries.html")
