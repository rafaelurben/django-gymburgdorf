from django.contrib import admin

from .models import Info, NotenManager, Semester, Fach, Note, Teilnote, UserContent

from .my23h import admin as _23h_admin

# Register your models here.

# Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Infos',       {'fields': ['title', 'text']}),
        ('Einstellungen',       {'fields': ['hidden']}),
    ]

    list_display = ["title", "text", "hidden"]
    list_filter = ["hidden"]

    ordering = ("title",)

# Noten


class NotenAdminTeilnotenInline(admin.TabularInline):
    model = Teilnote
    extra = 0
    fields = ("title", "value", "weight",)


@admin.register(Note)
class NotenAdmin(admin.ModelAdmin):
    list_display = ("title", "saved_value", "weight", "is_partial_grade",)
    readonly_fields = ("saved_value",)
    ordering = ("title",)

    def get_fields(self, request, obj=None):
        if obj and obj.is_partial_grade:
            return ("title", "weight", "is_partial_grade", "saved_value")
        else:
            return ("title", "value", "weight", "is_partial_grade",)

    def get_inlines(self, request, obj=None):
        return (NotenAdminTeilnotenInline,) if obj and obj.is_partial_grade else []

    def has_add_permission(self, request):
        return False

    def has_module_permission(self, request):
        return {}

    @admin.action(description="Gespeicherten Wert aktualisieren")
    def resave(self, request, queryset):
        for obj in queryset.all():
            obj.save()


class FachAdminNotenInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = ("url", "title", "value", "weight",
              "is_partial_grade", "saved_value",)

    readonly_fields = ("url", "saved_value",)


@admin.register(Fach)
class FachAdmin(admin.ModelAdmin):
    fields = ("title", "weight", "saved_value",)
    readonly_fields = ("saved_value",)
    list_display = ("title", "weight", "saved_value",)
    ordering = ("title",)

    inlines = (FachAdminNotenInline,)

    def has_add_permission(self, request):
        return False

    def has_module_permission(self, request):
        return {}

    @admin.action(description="Gespeicherten Wert aktualisieren")
    def resave(self, request, queryset):
        for obj in queryset.all():
            obj.save()


class SemesterAdminFachInline(admin.TabularInline):
    model = Fach
    extra = 0
    fields = ("url", "title", "weight", "saved_value",)
    readonly_fields = ("url", "saved_value",)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    fields = ("title", "saved_value",)
    readonly_fields = ("saved_value", )
    list_display = ("title", "saved_value",)
    ordering = ("title",)

    inlines = (SemesterAdminFachInline,)

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return {}

    @admin.action(description="Gespeicherten Wert aktualisieren")
    def resave(self, request, queryset):
        for obj in queryset.all():
            obj.save()


class NotenManagerAdminSemesterInline(admin.TabularInline):
    model = Semester
    extra = 0
    fields = ("url", "title", "saved_value",)
    readonly_fields = ("url", "saved_value",)


@admin.register(NotenManager)
class NotenManagerAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display = ("user",)
    ordering = ("user",)

    inlines = (NotenManagerAdminSemesterInline,)

    actions = ["resave"]

    @admin.action(description="Gespeicherten Wert aktualisieren")
    def resave(self, request, queryset):
        for obj in queryset.all():
            obj.save()

# Sprüche


@admin.register(UserContent)
class UserContentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Infos', {'fields': ['titel', 'beschreibung', 'personen']}),
        ('Daten', {'fields': ['published', 'published_at']}),
        ('Einstellungen', {'fields': ['user', 'kategorie']})
    ]
    readonly_fields = ['published_at']
    autocomplete_fields = ['user']

    list_display = ['id', 'titel', 'beschreibung', 'personen', 'user']

