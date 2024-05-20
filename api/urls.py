from rest_framework.urls import path
from api import views
app_name = "api"

urlpatterns = [
    path("api/accounts/details", views.AccountsDetailsView.as_view(), name="accouts_details")
]