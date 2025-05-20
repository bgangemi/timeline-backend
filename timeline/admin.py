from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Group, AbuseType, Event, EventFile, Comment

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at"]

@admin.register(AbuseType)
class AbuseTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "color"]
    search_fields = ["name"]

class EventFileInline(admin.TabularInline):
    model = EventFile
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["date", "name", "group", "abuse_types_display", "created_at"]
    list_filter = ["group", "abuse_types", "date"]
    search_fields = ["name", "description", "details"]
    filter_horizontal = ["abuse_types"]
    inlines = [EventFileInline]

    def abuse_types_display(self, obj):
        return ", ".join([at.name for at in obj.abuse_types.all()])
    abuse_types_display.short_description = "Abuse Types"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("timeline/", self.admin_site.admin_view(self.timeline_view), name="timeline"),
        ]
        return custom_urls + urls

    def timeline_view(self, request):
        groups = Group.objects.prefetch_related("events__abuse_types", "events__files", "events__comments").all()
        return render(request, "admin/timeline/timeline.html", {"groups": groups})

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["event", "user", "comment", "date"]
    list_filter = ["event", "user", "date"]
    search_fields = ["comment"]

admin.site.register(EventFile)