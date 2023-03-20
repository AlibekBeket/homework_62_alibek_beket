from django.contrib import admin

from issue_tracker.models import *


# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")
    list_filter = ("id", "type_name")
    search_fields = ("id", "type_name")
    fields = ("type_name",)
    readonly_fields = ("id",)


admin.site.register(Type, TypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status_name")
    list_filter = ("id", "status_name")
    search_fields = ("id", "status_name")
    fields = ("status_name",)
    readonly_fields = ("id",)


admin.site.register(Status, StatusAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "summary", "description", "status", "created_at", "updated_at", "project")
    list_filter = ("id", "summary", "description", "status", "created_at", "updated_at", "project")
    search_fields = ("id", "summary", "description", "status", "type", "project")
    fields = ("summary", "description", "status", "type", "created_at", "updated_at", "project")
    readonly_fields = ("id", "created_at", "updated_at")


admin.site.register(Issue, IssueAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "start_date", "end_date", "is_deleted")
    list_filter = ("id", "name", "description", "start_date", "end_date", "is_deleted")
    search_fields = ("id", "name", "description", "is_deleted")
    fields = ("name", "description", "start_date", "end_date", "is_deleted")
    readonly_fields = ("id", "start_date", "end_date")


admin.site.register(Project, ProjectAdmin)
