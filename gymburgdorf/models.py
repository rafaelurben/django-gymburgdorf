# pylint: disable=no-member

from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.html import mark_safe
from django.urls import reverse

from .utils import durchschnitt, htmlurl

from .my23h import models as _23h_models

# Create your models here.

# Info


class Info(models.Model):
    date_created = models.DateTimeField("Erstellt am", auto_now_add=True)
    date_updated = models.DateTimeField("Geändert am", auto_now=True)

    title = models.CharField("Titel", max_length=50)
    text = models.TextField("Text")

    hidden = models.BooleanField("Versteckt", default=False)

    def html_text(self):
        return mark_safe(self.text)

    @admin.display(description="Info")
    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Information"
        verbose_name_plural = "Informationen"

    objects = models.Manager()


# Noten

class NotenManager(models.Model):
    date_created = models.DateTimeField("Erstellt am", auto_now_add=True)
    date_updated = models.DateTimeField("Geändert am", auto_now=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gymburgdorf_notenmanager")

    def json(self):
        return {
            "type": "grademanager",
            "id": self.pk,
            "info": f"Eingeloggt als: {self.user.username}",
            "semesters": [
                semester.json(withsub=False) for semester in self.semesters.all().order_by("title")
            ]
        }

    @admin.display(description="Notenmanager")
    def __str__(self):
        return f"Notenmanager von {self.user.username}"

    class Meta:
        verbose_name = "Notenmanager"
        verbose_name_plural = "Notenmanager"

    objects = models.Manager()


class Semester(models.Model):
    date_created = models.DateTimeField("Erstellt am", auto_now_add=True)
    date_updated = models.DateTimeField("Geändert am", auto_now=True)

    manager = models.ForeignKey(
        NotenManager, on_delete=models.CASCADE, related_name="semesters")

    title = models.CharField("Name", max_length=50)

    saved_value = models.FloatField("Notenwert", validators=[MinValueValidator(
        1.0), MaxValueValidator(6.0)], default=None, null=True)

    def json(self, withsub=True):
        data = {
            "type": "semester",
            "id": self.pk,
            "title": self.title,
            "value": self.saved_value,
            "info": f"Note: {self.saved_value}",
        }
        if withsub:
            data["subjects"] = [
                subject.json(withsub=False) for subject in self.subjects.all().order_by("title")
            ]
        return data

    def save(self, *args, **kwargs):
        self.saved_value = durchschnitt(
            [(subject.saved_value, subject.weight) for subject in self.subjects.all() if subject.saved_value is not None])
        super().save(*args, **kwargs)

    @property
    def url(self):
        return htmlurl(reverse("admin:gymburgdorf_semester_change", args=(self.pk,))) if self.pk else ""

    @admin.display(description="Semester")
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semester"

    objects = models.Manager()


class Fach(models.Model):
    date_created = models.DateTimeField("Erstellt am", auto_now_add=True)
    date_updated = models.DateTimeField("Geändert am", auto_now=True)

    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="subjects")

    title = models.CharField("Name", max_length=50, default="")

    weight = models.FloatField("Gewicht", default=1)

    saved_value = models.FloatField("Notenwert", validators=[MinValueValidator(
        1.0), MaxValueValidator(6.0)], default=None, null=True)

    def json(self, withsub=True):
        data = {
            "type": "subject",
            "id": self.pk,
            "title": self.title,
            "weight": self.weight,
            "value": self.saved_value,
            "info": f"Note: {self.saved_value} - Gewicht: {self.weight}",
        }
        if withsub:
            data["grades"] = [
                grade.json(withsub=False) for grade in self.grades.all().order_by("title")
            ]
        return data

    def save(self, *args, **kwargs):
        self.saved_value = durchschnitt(
            [(grade.saved_value, grade.weight) for grade in self.grades.all() if grade.saved_value is not None])
        super().save(*args, **kwargs)
        self.semester.save()

    @property
    def url(self):
        return htmlurl(reverse("admin:gymburgdorf_fach_change", args=(self.pk,))) if self.pk else ""

    @admin.display(description="Fach")
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Fach"
        verbose_name_plural = "Fächer"

    objects = models.Manager()


class Note(models.Model):
    date_created = models.DateTimeField("Erstellt am", auto_now_add=True)
    date_updated = models.DateTimeField("Geändert am", auto_now=True)

    subject = models.ForeignKey(
        Fach, on_delete=models.CASCADE, related_name="grades")

    title = models.CharField("Name", max_length=50, default="")

    is_partial_grade = models.BooleanField("Teilnote?", default=False)
    weight = models.FloatField("Gewicht", default=1)

    value = models.FloatField("Note", validators=[MinValueValidator(
        1.0), MaxValueValidator(6.0)], blank=True, default=None, null=True)

    saved_value = models.FloatField("Notenwert", validators=[MinValueValidator(
        1.0), MaxValueValidator(6.0)], default=None, null=True)

    def json(self, withsub=True):
        data = {
            "type": "grade",
            "id": self.pk,
            "title": self.title,
            "weight": self.weight,
            "value": self.saved_value,
            "is_partial_grade": True,
            "info": f"Note: {self.saved_value} - Gewicht: {self.weight}",
        }
        if self.is_partial_grade and withsub:
            data["partial_grades"] = [
                partialgrade.json() for partialgrade in self.partial_grades.all().order_by("title")
            ]
        return data

    def save(self, *args, **kwargs):
        if self.is_partial_grade:
            self.saved_value = durchschnitt(
                [(teilnote.value, teilnote.weight) for teilnote in self.partial_grades.all() if teilnote.value is not None])
        else:
            self.saved_value = self.value
        super().save(*args, **kwargs)
        self.subject.save()

    @property
    def url(self):
        return htmlurl(reverse("admin:gymburgdorf_note_change", args=(self.pk,))) if self.pk and self.is_partial_grade else ""

    @admin.display(description="Note")
    def __str__(self):
        return f"{self.title} ({self.saved_value}*{self.weight})" if not self.is_partial_grade else f"{self.title} (<Teilnote: {self.saved_value}>*{self.weight})"

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Noten"

    objects = models.Manager()


class Teilnote(models.Model):
    date_created = models.DateTimeField("Erstellt am", auto_now_add=True)
    date_updated = models.DateTimeField("Geändert am", auto_now=True)

    grade = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name="partial_grades")

    title = models.CharField("Name", max_length=50, default="")

    weight = models.FloatField("Gewicht", default=1)
    value = models.FloatField("Note", validators=[MinValueValidator(
        1.0), MaxValueValidator(6.0)], blank=True, default=None, null=True)

    def json(self):
        return {
            "type": "partial_grade",
            "id": self.pk,
            "title": self.title,
            "weight": self.weight,
            "value": self.value,
            "info": f"Note: {self.value} - Gewicht: {self.weight}",
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.grade.save()

    @admin.display(description="Teilnote")
    def __str__(self):
        return f"{self.title} ({self.value}*{self.weight})"

    class Meta:
        verbose_name = "Teilnote"
        verbose_name_plural = "Teilnoten"

    objects = models.Manager()

# Benutzerinhalte: Sprüche und Insider


class UserContent(models.Model):
    KATEGORIEN = [
        ("quote", "Zitat"),
        ("giftidea", "Geschenkidee"),
    ]

    titel = models.CharField("Titel", max_length=50)
    beschreibung = models.TextField("Beschreibung")
    personen = models.CharField("Personen", max_length=250)
    kategorie = models.CharField(
        "Kategorie", max_length=20, choices=KATEGORIEN)

    published = models.BooleanField("Veröffentlicht?", default=False)
    published_at = models.DateTimeField(
        "Veröffentlicht um", blank=True, null=True)

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gymburgdorf_sprueche",
    )

    def json(self, request=None):
        data = {
            "id": self.id,
            "titel": self.titel,
            "beschreibung": self.beschreibung,
            "personen": self.personen,
            "kategorie": self.kategorie,
            "kategorie_display": self.get_kategorie_display(),
            "username": self.user.username,
            "published": self.published,
            "published_at": str(self.published_at),
            "_fullinfo": f"Titel:\n{self.titel}\n\nBeschreibung:\n{self.beschreibung}\n\n"
                         f"Personen:\n{self.personen}",
        }
        if request:
            data["candelete"] = (
                request.user.has_perm('gymburgdorf.delete_usercontent') or (
                    request.user == self.user and not self.published))
            data["canpublish"] = (
                not self.published and request.user.has_perm('gymburgdorf.publish_usercontent'))
            data["canchange"] = (
                request.user.has_perm('gymburgdorf.change_usercontent'))
        return data

    @admin.display(description="UserContent")
    def __str__(self):
        return f'{self.titel} - {self.user.username}'

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.published and not self.published_at:
            self.published_at = timezone.now()
            self.save()
        elif self.published_at and not self.published:
            self.published_at = None
            self.save()

    class Meta:
        verbose_name = "Benutzerinhalt"
        verbose_name_plural = "Benutzerinhalte"
        default_permissions = ('change', 'publish', 'delete')

