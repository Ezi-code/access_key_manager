from rest_framework.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path(
        "accounts/details",
        views.AccountsDetails.as_view(),
        name="accouts_details",
    ),
]
