from django.urls import path
from tasks import views

urlpatterns = [
    path("create/sync", views.create_task_sync, name="create_task_sync"),
]
