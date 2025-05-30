from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from .models import File, Group, Event, UploadedDocument, Tag   
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

class UploadedDocumentInline(GenericTabularInline):
    model = UploadedDocument
    extra = 0

class EventInline(admin.TabularInline):
    model = Event
    fields = ('name', 'date', 'date_approx_level') 
    extra = 0

class GroupInline(admin.TabularInline):
    model = Group
    fields = ('view_link', 'name', 'description', 'date_start', 'date_end')
    readonly_fields = ('view_link', 'date_start', 'date_end')
    extra = 0
    ordering = ['date_start']

    def view_link(self, obj):
        if obj.pk:
            app_label = obj._meta.app_label
            model_name = obj._meta.model_name
            url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
            return format_html('<a href="{}">-> Edit Group</a>', url)
        return "-"
    
    view_link.short_description = 'Edit Group'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "created_at", "group_count", "event_count"]
    inlines = [GroupInline, UploadedDocumentInline]
    autocomplete_fields = ['tags']

    def group_count(self, obj):
        return obj.group_set.count()
    group_count.short_description = 'Groups'

    def event_count(self, obj):
        return Event.objects.filter(file=obj).count()
    event_count.short_description = 'Events'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['__str__', "date_start", "date_end", "name", "owner", "rendered_description", "file", "created_at"]
    inlines = [EventInline, UploadedDocumentInline]
    autocomplete_fields = ['tags']

    def rendered_description(self, obj):
        return mark_safe(obj.description) if obj.description else ''
    rendered_description.short_description = "Description"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["date", "name", "owner", "group", "rendered_description"]
    list_filter = ["date", "owner", "group", "file"]
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
