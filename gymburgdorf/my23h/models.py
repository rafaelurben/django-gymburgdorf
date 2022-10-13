from django.db import models
from django.db.models.functions import Cast
from django.conf import settings


# Maturabücher

class MaturaBookSelection(models.Model):
    MAX_RESERVATIONS_PER_BOOK = 3
    MAX_RESERVATIONS_PER_USER = 6

    TYPES = [
        ('reserved', "reserviert"),
        ('presaved', "vorgemerkt")
    ]
    TYPE_LIST = [a[0] for a in TYPES]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gymburgdorf_maturabook_selections")
    book = models.CharField("Buch", max_length=50)

    typ = models.CharField("Typ", max_length=50, choices=TYPES, default='presaved')

    is_removed = models.BooleanField("Gelöscht", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def is_reservation_possible_for_user(cls, user):
        return cls.objects.filter(user=user, is_removed=False, typ='reserved').count() < cls.MAX_RESERVATIONS_PER_USER

    @classmethod
    def is_reservation_possible_for_book(cls, book):
        return cls.objects.filter(book=book, is_removed=False, typ='reserved').count() < cls.MAX_RESERVATIONS_PER_BOOK

    @classmethod
    def getselectionsforuser(cls, user, **filter):
        return list(MaturaBookSelection.objects.filter(user=user, is_removed=False, **filter).order_by('book').all())

    @classmethod
    def getuserbooklist(cls, user):
        booklist = {}
        for selection in cls.objects.filter(is_removed=False).select_related('user').all():
            if not selection.book in booklist:
                booklist[selection.book] = {
                    "title": selection.book,
                    "count_reserved": 0,
                    "count_presaved": 0,
                    "can_reserve": True,
                    "onmylist": False,
                    "users_presaved": [],
                    "users_reserved": [],
                }

            if selection.typ == "reserved":
                booklist[selection.book]["count_reserved"] += 1
                booklist[selection.book]['users_reserved'].append(selection.user.username)
            elif selection.typ == "presaved":
                booklist[selection.book]["count_presaved"] += 1
                booklist[selection.book]['users_presaved'].append(selection.user.username)

            if booklist[selection.book]["count_reserved"] >= cls.MAX_RESERVATIONS_PER_BOOK:
                booklist[selection.book]["can_reserve"] = False

            if selection.user == user:
                booklist[selection.book]["onmylist"] = selection.typ
        return sorted(booklist.values(), key=lambda x: x["title"])

    def softremove(self):
        self.is_removed = True
        self.save()

    class Meta:
        verbose_name = "Maturbuchreservation"
        verbose_name_plural = "Maturbuchreservationen"

# MULUS-Sammlung

class MulusCollectionPerson(models.Model):
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)

    quotes = models.ManyToManyField(to="MulusCollectionQuote", through="MulusCollectionPersonQuoteRelation")

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "MULUS-Sammlung: Person"
        verbose_name_plural = "MULUS-Sammlung: Personen"

    objects = models.Manager()

    def __str__(self) -> str:
        return self.name

class MulusCollectionQuote(models.Model):
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    people = models.ManyToManyField(to="MulusCollectionPerson", through="MulusCollectionPersonQuoteRelation")

    class Meta:
        verbose_name = "MULUS-Sammlung: Zitat"
        verbose_name_plural = "MULUS-Sammlung: Zitate"

    def person_names(self):
        return ", ".join([p.name for p in self.people.all()])

    objects = models.Manager()

    def __str__(self) -> str:
        return self.content[:50]

    @classmethod
    def get_quotes_with_reviews(cls, user):
        return cls.objects.all().prefetch_related(
            'reviews', 'created_by', 'people'
        ).annotate(
            total_likes=models.Sum(models.Case(models.When(reviews__like=True, then=1), default=0)),
            total_dislikes=models.Sum(models.Case(models.When(reviews__like=False, then=1), default=0)),
            total_reviews=models.Count('reviews'),
            user_review_like=models.Sum(models.Case(models.When(reviews__user_id=user.pk, then=models.Case(models.When(reviews__like=True, then=1), default=0)), default=None)),
        ).annotate(
            percentage_likes=Cast('total_likes', models.FloatField())/Cast('total_reviews', models.FloatField())
        ).order_by('-percentage_likes', '-total_likes')

class MulusCollectionPersonQuoteRelation(models.Model):
    quote = models.ForeignKey(to="MulusCollectionQuote", on_delete=models.CASCADE)
    person = models.ForeignKey(to="MulusCollectionPerson", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MULUS-Sammlung: Zitat-Person-Verbindung"
        verbose_name_plural = "MULUS-Sammlung: Zitat-Person-Verbindungen"

    objects = models.Manager()

    def __str__(self) -> str:
        return f"Verbindung #{self.id}"

class MulusCollectionQuoteReview(models.Model):
    quote = models.ForeignKey(to="MulusCollectionQuote", related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='gymburgdorf_muluscollection_quotereviews', on_delete=models.CASCADE)

    like = models.BooleanField(default=True)

    class Meta:
        verbose_name = "MULUS-Sammlung: Zitat-Bewertung"
        verbose_name_plural = "MULUS-Sammlung: Zitat-Bewertungen"

    objects = models.Manager()

    def __str__(self) -> str:
        return f"Bewertung #{self.id}"
