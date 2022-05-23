from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Transaction


@require_http_methods(["GET"])
def profitsandlosses(request):
    transactions = Transaction.objects.all().order_by("category", "sub_category")
    months = transactions.dates("date", "month")

    return render(
        request,
        "profits_and_losses.html",
        {"months": months, "transactions": transactions},
    )
