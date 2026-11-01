from django.contrib import admin

from .models import Company, Contact, Deal, Lead, Pipeline, Stage


class StageInline(admin.TabularInline):
    model = Stage
    extra = 1
    fields = ("name", "order", "color", "is_won", "is_lost")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "owner", "created_at")
    list_filter = ("industry",)
    search_fields = ("name", "email", "phone")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name",
                    "company", "email", "is_primary")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("is_primary",)


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("name", "is_default", "organization")
    inlines = [StageInline]


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("name", "pipeline", "order", "is_won", "is_lost")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "source", "owner")
    list_filter = ("status", "source")
    search_fields = ("title", "company__name")


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "stage", "status", "amount", "owner")
    list_filter = ("status", "pipeline", "stage")
    search_fields = ("title", "company__name")
