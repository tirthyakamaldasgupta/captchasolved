from django.urls import path
from tasks import views

urlpatterns = [
    path("create", views.create_task, name="create_task"),
]
