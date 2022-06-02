from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path("", RedirectView.as_view(url="transactions/pl")),
    path("health/", views.health),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("transactions/", include("transactions.urls")),
]
