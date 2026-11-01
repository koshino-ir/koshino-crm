from django.urls import path

from .views import AttachmentDetailView, AttachmentDownloadView, AttachmentListCreateView

app_name = "attachments"

urlpatterns = [
    path("attachments/", AttachmentListCreateView.as_view(), name="attachment-list"),
    path("attachments/<uuid:attachment_id>/",
         AttachmentDetailView.as_view(), name="attachment-detail"),
    path("attachments/<uuid:attachment_id>/download/",
         AttachmentDownloadView.as_view(), name="attachment-download"),
]
