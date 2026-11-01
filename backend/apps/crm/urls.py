from django.urls import path

from .views.company import CompanyDetailView, CompanyListCreateView
from .views.contact import ContactDetailView, ContactListCreateView
from .views.deal import (
    DealDetailView, DealKanbanView, DealListCreateView, DealMoveView,
)
from .views.lead import LeadConvertView, LeadDetailView, LeadListCreateView
from .views.search import GlobalSearchView
from .views.pipeline import (
    PipelineDetailView, PipelineEnsureDefaultView, PipelineListCreateView,
    StageDetailView, StageListCreateView,
)

app_name = "crm"

urlpatterns = [
    # Companies
    path("companies/", CompanyListCreateView.as_view(), name="company-list"),
    path("companies/<uuid:company_id>/",
         CompanyDetailView.as_view(), name="company-detail"),

    # Contacts
    path("contacts/", ContactListCreateView.as_view(), name="contact-list"),
    path("contacts/<uuid:contact_id>/",
         ContactDetailView.as_view(), name="contact-detail"),

    # Pipelines & Stages
    path("pipelines/", PipelineListCreateView.as_view(), name="pipeline-list"),
    path("pipelines/ensure-default/", PipelineEnsureDefaultView.as_view(),
         name="pipeline-ensure-default"),
    path("pipelines/<uuid:pipeline_id>/",
         PipelineDetailView.as_view(), name="pipeline-detail"),
    path("pipelines/<uuid:pipeline_id>/stages/",
         StageListCreateView.as_view(), name="stage-list"),
    path("stages/<uuid:stage_id>/", StageDetailView.as_view(), name="stage-detail"),

    # Leads
    path("leads/", LeadListCreateView.as_view(), name="lead-list"),
    path("leads/<uuid:lead_id>/", LeadDetailView.as_view(), name="lead-detail"),
    path("leads/<uuid:lead_id>/convert/",
         LeadConvertView.as_view(), name="lead-convert"),

    # Deals
    path("deals/", DealListCreateView.as_view(), name="deal-list"),
    path("deals/kanban/", DealKanbanView.as_view(), name="deal-kanban"),
    path("deals/<uuid:deal_id>/", DealDetailView.as_view(), name="deal-detail"),
    path("deals/<uuid:deal_id>/move/", DealMoveView.as_view(), name="deal-move"),

    # search
    path("search/", GlobalSearchView.as_view(), name="global-search"),
]
