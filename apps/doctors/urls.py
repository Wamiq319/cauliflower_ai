from django.urls import path
from . import views

urlpatterns = [
    path("suggestions/create/", views.create_suggestion, name="doctor_create_suggestion"),
]
