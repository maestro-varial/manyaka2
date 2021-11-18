from django.urls import path
from . import views


app_name = "vendor"

urlpatterns = [
    path("", views.VendorViewAPI.as_view(), name="VendorViewAPI"),
    path("withdrawn/", views.WithdrawnViewAPI.as_view(), name="WithdrawnViewAPI")
]
