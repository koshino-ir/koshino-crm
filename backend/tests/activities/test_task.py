import pytest

from apps.activities.models import Task


@pytest.mark.django_db
def test_create_task(auth_client, organization):
    resp = auth_client.post(
        "/api/v1/tasks/",
        {"title": "Follow up", "priority": "high"},
        format="json",
    )
    assert resp.status_code == 201
    assert Task.objects.filter(title="Follow up").exists()


@pytest.mark.django_db
def test_complete_task(auth_client, organization):
    task = Task.objects.create(organization=organization, title="X")
    resp = auth_client.post(f"/api/v1/tasks/{task.id}/complete/")
    assert resp.status_code == 200
    task.refresh_from_db()
    assert task.status == Task.Status.DONE
    assert task.completed_at is not None


@pytest.mark.django_db
def test_filter_tasks_by_status(auth_client, organization):
    Task.objects.create(organization=organization,
                        title="A", status=Task.Status.DONE)
    Task.objects.create(organization=organization,
                        title="B", status=Task.Status.TODO)
    resp = auth_client.get("/api/v1/tasks/?status=todo")
    assert resp.status_code == 200
    titles = [t["title"] for t in resp.json()["data"]]
    assert titles == ["B"]
