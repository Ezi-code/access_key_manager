from django.urls import path
from main import views


app_name = "main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("request_key/<uuid>", views.RequestKeyView.as_view(), name="request_key"),
]
