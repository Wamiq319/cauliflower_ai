from django.urls import path
from .views import detect_disease_view, open_case_view

urlpatterns = [
    path("detect/", detect_disease_view, name="farmer_detect_disease"),
    path("open-case/", open_case_view, name="farmer_open_case"),
]
