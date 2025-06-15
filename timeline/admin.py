from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from .models import File, Event, UploadedDocument, Tag, Comment   
from django.utils.safestring import mark_safe

class UploadedDocumentInline(GenericTabularInline):
    model = UploadedDocument
    extra = 0

class EventInline(admin.TabularInline):
    model = Event
    fields = ('name', 'date', 'date_approx_level') 
    extra = 0

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['comment']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["indented_name", "parent", "owner", "created_at", "event_count"]
    inlines = [UploadedDocumentInline]
    autocomplete_fields = ['tags']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Order by parent (nulls first), then by name
        return qs.order_by('parent__id', 'name')

    def indented_name(self, obj):
        # Indent by level of nesting - count ancestors recursively
        level = 0
        parent = obj.parent
        while parent:
            level += 1
            parent = parent.parent
        indent = "— " * level
        return f"{indent}{obj.name}"
    indented_name.short_description = "Name"
    indented_name.admin_order_field = 'name'

    def event_count(self, obj):
        return Event.objects.filter(file=obj).count()
    event_count.short_description = 'Events'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["date", "file", "name", "owner", "rendered_description"]
    list_filter = ["date", "owner", "file"]
    ordering = ["date"]
    inlines = [UploadedDocumentInline]
    autocomplete_fields = ['tags']

    def rendered_description(self, obj):
        return mark_safe(obj.description) if obj.description else ''
    rendered_description.short_description = "Description"

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'document', 'uploaded_at']
    autocomplete_fields = ['tags']
