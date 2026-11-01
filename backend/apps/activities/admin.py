from django.contrib import admin

from .models import Activity, Task


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("type", "subject", "occurred_at", "created_by")
    list_filter = ("type",)
    search_fields = ("subject", "description")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "due_date", "assigned_to")
    list_filter = ("status", "priority")
    search_fields = ("title", "description")
