from django.urls import path

from .views import (
    ActivityDetailView, ActivityListCreateView,
    TaskCompleteView, TaskDetailView, TaskListCreateView, TaskReopenView,
)

app_name = "activities"

urlpatterns = [
    path("activities/", ActivityListCreateView.as_view(), name="activity-list"),
    path("activities/<uuid:activity_id>/",
         ActivityDetailView.as_view(), name="activity-detail"),

    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<uuid:task_id>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<uuid:task_id>/complete/",
         TaskCompleteView.as_view(), name="task-complete"),
    path("tasks/<uuid:task_id>/reopen/",
         TaskReopenView.as_view(), name="task-reopen"),
]
