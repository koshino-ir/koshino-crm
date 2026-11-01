from django.contrib import admin

from .models import Invoice, Project


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    fields = ("number", "amount", "tax", "total",
              "status", "issue_date", "due_date")
    readonly_fields = ("total",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "client_company", "owner", "budget")
    list_filter = ("status",)
    search_fields = ("name", "client_company__name")
    inlines = [InvoiceInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "project", "total", "status", "due_date")
    list_filter = ("status",)
    search_fields = ("number", "project__name")
