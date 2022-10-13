from django.contrib import admin

from .models import MaturaBookSelection, MulusCollectionPerson, MulusCollectionQuote

# Register your models here.

# Maturabücher

@admin.register(MaturaBookSelection)
class MaturaBookSelectionAdmin(admin.ModelAdmin):
    fields = ["book", "user"]

    list_display = ['id', 'typ', 'book', 'user', 'created_at', 'is_removed']
    list_filter = ['is_removed']
    autocomplete_fields = ['user']

# MULUS-Sammlung

class MulusCollectionPersonQuoteInline(admin.TabularInline):
    model = MulusCollectionPerson.quotes.through
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(MulusCollectionPerson)
class MulusCollectionPersonAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': [('first_name', 'last_name')]})]

    list_display = ['id', 'first_name', 'last_name']

    inlines = [MulusCollectionPersonQuoteInline]

    def get_inlines(self, request, obj):
        if obj is None:
            return []
        return super().get_inlines(request, obj)

class MulusCollectionQuotePersonInline(admin.TabularInline):
    model = MulusCollectionQuote.people.through
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(MulusCollectionQuote)
class MulusCollectionQuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'person_names']
    readonly_fields = ['created_at', 'created_by']

    inlines = [MulusCollectionQuotePersonInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('people')

    def get_fields(self, request, obj):
        if not getattr(obj, 'pk', None):
            return ['content']
        else:
            return ['content', 'created_by', 'created_at']

    def save_model(self, request, obj, form, change) -> None:
        if not getattr(obj, 'pk', None):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
