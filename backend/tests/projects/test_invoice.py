import pytest

from apps.projects.models import Invoice, Project


@pytest.fixture
def project(db, organization, company, user):
    return Project.objects.create(
        organization=organization, name="P", client_company=company, owner=user,
    )


@pytest.mark.django_db
def test_create_invoice_generates_number_and_total(
    auth_client, organization, project
):
    resp = auth_client.post(
        "/api/v1/invoices/",
        {
            "project_id": str(project.id),
            "amount": "1000.00",
            "tax": "90.00",
            "issue_date": "2026-01-01",
            "due_date": "2026-01-31",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    data = resp.json()["data"]
    assert data["number"].startswith("INV-")
    assert float(data["total"]) == 1090.00


@pytest.mark.django_db
def test_invoice_number_unique_per_org(auth_client, organization, project):
    for _ in range(2):
        resp = auth_client.post(
            "/api/v1/invoices/",
            {
                "project_id": str(project.id),
                "amount": "100.00",
                "issue_date": "2026-01-01",
                "due_date": "2026-01-31",
            },
            format="json",
        )
        assert resp.status_code == 201
    numbers = set(Invoice.objects.values_list("number", flat=True))
    assert len(numbers) == 2


@pytest.mark.django_db
def test_mark_paid(auth_client, organization, project):
    inv = Invoice.objects.create(
        organization=organization, project=project,
        number="INV-2026-0001", amount="100.00",
        issue_date="2026-01-01", due_date="2026-01-31",
    )
    resp = auth_client.post(f"/api/v1/invoices/{inv.id}/mark-paid/")
    assert resp.status_code == 200
    inv.refresh_from_db()
    assert inv.status == Invoice.Status.PAID
    assert inv.paid_at is not None


@pytest.mark.django_db
def test_due_before_issue_rejected(auth_client, organization, project):
    resp = auth_client.post(
        "/api/v1/invoices/",
        {
            "project_id": str(project.id),
            "amount": "100.00",
            "issue_date": "2026-02-01",
            "due_date": "2026-01-01",
        },
        format="json",
    )
    assert resp.status_code == 400
