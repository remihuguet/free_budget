from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_transaction, name="add_transaction"),
    path("<int:id>", views.edit_transaction, name="edit_transaction"),
    path("pl", views.profitsandlosses, name="pandl"),
]
