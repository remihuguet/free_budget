from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import routers
from . import views, api

api_router = routers.DefaultRouter()
api_router.register(r"subcategories", api.SubcategoryViewSet)

urlpatterns = [
    path(
        "",
        permission_required("transactions.add_transaction")(
            views.TransactionForm.as_view()
        ),
        name="add_transaction",
    ),
    path("api/", include(api_router.urls)),
    path(
        "<int:id>",
        permission_required("transactions.change_transaction")(
            views.EditTransactionForm.as_view()
        ),
        name="edit_transaction",
    ),
    path(
        "subcategories",
        login_required(views.SubCategoriesView.as_view()),
        name="subcategories",
    ),
    path(
        "subcategories/create",
        login_required(views.AddSubCategoryView.as_view()),
        name="add_subcategory",
    ),
    path(
        "subcategories/<int:pk>",
        login_required(views.UpdateSubCategoryView.as_view()),
        name="update_subcategory",
    ),
    path(
        "subcategories/<int:pk>/delete",
        login_required(views.DeleteSubCategoryView.as_view()),
        name="delete_subcategory",
    ),
    path("pl", login_required(views.ProfitsAndLossesView.as_view()), name="pandl"),
]
