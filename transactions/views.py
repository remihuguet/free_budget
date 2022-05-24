from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from transactions.forms import AddTransactionForm
from .models import Transaction


@require_http_methods(["GET"])
def profitsandlosses(request):
    transactions = Transaction.objects.all().order_by(
        "category", "sub_category", "label"
    )
    months = transactions.dates("date", "month")
    ref_months = [f"{m.year}{m.month}" for m in months]
    p_and_l = []
    line = None
    for transac in transactions:
        if not line or transac.label != line["label"]:
            if line:
                p_and_l.append(line)
            line = {
                "label": transac.label,
                "category": transac.get_category_display(),
                "sub_category": transac.sub_category.name
                if transac.sub_category
                else "",
            }
            line["amounts"] = ["" for month in ref_months]

        line["amounts"][
            ref_months.index(f"{transac.date.year}{transac.date.month}")
        ] = transac.total_amount

    return render(
        request,
        "profits_and_losses.html",
        {
            "months": months,
            "pandl": p_and_l,
            "ref_months": ref_months,
        },
    )


@require_http_methods(["GET", "POST"])
def add_transaction(request):
    if request.method == "POST":
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            transaction = Transaction(**form.cleaned_data)
            transaction.save()
            messages.info(request, f"Transaction {transaction} created")
        else:
            return render(request, "add_transaction.html", {"form": form})
    form = AddTransactionForm()
    return render(request, "add_transaction.html", {"form": form})
