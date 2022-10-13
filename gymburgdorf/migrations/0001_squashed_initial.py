# Generated by Django 4.1 on 2022-10-13 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MaturaBookSelection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("book", models.CharField(max_length=50, verbose_name="Buch")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gymburgdorf_maturabook_selections",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "is_removed",
                    models.BooleanField(default=False, verbose_name="Gelöscht"),
                ),
                (
                    "typ",
                    models.CharField(
                        choices=[
                            ("reserved", "reserviert"),
                            ("presaved", "vorgemerkt"),
                        ],
                        default="presaved",
                        max_length=50,
                        verbose_name="Typ",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Maturbuchreservation",
                "verbose_name_plural": "Maturbuchreservationen",
            },
        ),
        migrations.CreateModel(
            name="MulusCollectionPerson",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_name", models.CharField(max_length=25)),
                ("first_name", models.CharField(max_length=25)),
            ],
            options={
                "verbose_name": "MULUS-Sammlung: Person",
                "verbose_name_plural": "MULUS-Sammlung: Personen",
            },
        ),
        migrations.CreateModel(
            name="MulusCollectionPersonQuoteRelation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gymburgdorf.muluscollectionperson",
                    ),
                ),
            ],
            options={
                "verbose_name": "MULUS-Sammlung: Zitat-Person-Verbindung",
                "verbose_name_plural": "MULUS-Sammlung: Zitat-Person-Verbindungen",
            },
        ),
        migrations.CreateModel(
            name="MulusCollectionQuote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("content", models.TextField()),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "people",
                    models.ManyToManyField(
                        through="gymburgdorf.MulusCollectionPersonQuoteRelation",
                        to="gymburgdorf.muluscollectionperson",
                    ),
                ),
            ],
            options={
                "verbose_name": "MULUS-Sammlung: Zitat",
                "verbose_name_plural": "MULUS-Sammlung: Zitate",
            },
        ),
        migrations.AddField(
            model_name="muluscollectionpersonquoterelation",
            name="quote",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="gymburgdorf.muluscollectionquote",
            ),
        ),
        migrations.AddField(
            model_name="muluscollectionperson",
            name="quotes",
            field=models.ManyToManyField(
                through="gymburgdorf.MulusCollectionPersonQuoteRelation",
                to="gymburgdorf.muluscollectionquote",
            ),
        ),
        migrations.CreateModel(
            name="MulusCollectionQuoteReview",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("like", models.BooleanField(default=True)),
                (
                    "quote",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="gymburgdorf.muluscollectionquote",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gymburgdorf_muluscollection_quotereviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "MULUS-Sammlung: Zitat-Bewertung",
                "verbose_name_plural": "MULUS-Sammlung: Zitat-Bewertungen",
            },
        ),
    ]
