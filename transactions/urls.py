from django.urls import path
from . import views

urlpatterns = [path("pl", views.profitsandlosses, name="pandl")]
