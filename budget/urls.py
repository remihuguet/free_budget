from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("health/", views.health),
    path("admin/", admin.site.urls),
    path("transactions/", include("transactions.urls")),
]
