import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.attachments.models import Attachment


@pytest.fixture
def project(db, organization, company, user):
    from apps.projects.models import Project as P
    return P.objects.create(
        organization=organization, name="P", client_company=company, owner=user,
    )


@pytest.mark.django_db
def test_upload_attachment_to_project(auth_client, organization, project):
    f = SimpleUploadedFile("report.pdf", b"%PDF-1.4 test",
                           content_type="application/pdf")
    resp = auth_client.post(
        "/api/v1/attachments/",
        {"file": f, "project_id": str(project.id)},
        format="multipart",
    )
    assert resp.status_code == 201, resp.content
    data = resp.json()["data"]
    assert data["original_name"] == "report.pdf"
    assert data["size"] == len(b"%PDF-1.4 test")
    assert data["download_url"].endswith("/download/")
    assert Attachment.objects.filter(organization=organization).count() == 1


@pytest.mark.django_db
def test_upload_rejects_unsupported_extension(auth_client, project):
    f = SimpleUploadedFile("evil.exe", b"malware",
                           content_type="application/octet-stream")
    resp = auth_client.post(
        "/api/v1/attachments/",
        {"file": f, "project_id": str(project.id)},
        format="multipart",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_upload_requires_exactly_one_target(auth_client, organization, company, project):
    f = SimpleUploadedFile("a.pdf", b"x", content_type="application/pdf")
    resp = auth_client.post(
        "/api/v1/attachments/",
        {
            "file": f,
            "project_id": str(project.id),
            "company_id": str(company.id),
        },
        format="multipart",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_download_attachment(auth_client, organization, project):
    f = SimpleUploadedFile("a.txt", b"hello", content_type="text/plain")
    att = Attachment.objects.create(
        organization=organization, file=f, original_name="a.txt",
        mime_type="text/plain", size=5, project=project,
    )
    resp = auth_client.get(f"/api/v1/attachments/{att.id}/download/")
    assert resp.status_code == 200
    assert b"".join(resp.streaming_content) == b"hello"
    assert resp["Content-Disposition"].startswith("attachment")
