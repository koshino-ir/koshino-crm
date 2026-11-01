from django.urls import path

from .views.invoice import (
    InvoiceDetailView, InvoiceListCreateView, InvoiceMarkPaidView,
)
from .views.project import ProjectDetailView, ProjectListCreateView

app_name = "projects"

urlpatterns = [
    path("projects/", ProjectListCreateView.as_view(), name="project-list"),
    path("projects/<uuid:project_id>/",
         ProjectDetailView.as_view(), name="project-detail"),

    path("invoices/", InvoiceListCreateView.as_view(), name="invoice-list"),
    path("invoices/<uuid:invoice_id>/",
         InvoiceDetailView.as_view(), name="invoice-detail"),
    path("invoices/<uuid:invoice_id>/mark-paid/",
         InvoiceMarkPaidView.as_view(), name="invoice-mark-paid"),
]
