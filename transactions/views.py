from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from transactions.forms import AddTransactionForm, EditTransactionForm
from .models import Transaction


@require_http_methods(["GET"])
@login_required
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
        ] = (transac.total_amount, resolve_url(to="edit_transaction", id=transac.id))

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
@login_required
@permission_required("transactions.add_transaction")
def add_transaction(request):
    if request.method == "POST":
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            transaction = Transaction(**form.cleaned_data)
            transaction.save()
            messages.info(request, f"Transaction {transaction} created")
            return redirect("pandl")
    else:
        form = AddTransactionForm()
    return render(request, "add_transaction.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
@permission_required("transactions.change_transaction")
def edit_transaction(request, id: int):
    transaction = get_object_or_404(Transaction.objects, id=id)
    if request.method == "POST":
        data = {k: v for k, v in request.POST.items()}
        data["id"] = transaction.id
        form = EditTransactionForm(request.POST)
        if form.is_valid():
            transaction.date = form.cleaned_data["date"]
            transaction.label = form.cleaned_data["label"]
            transaction.category = int(form.cleaned_data["category"])
            transaction.sub_category = form.cleaned_data["sub_category"]
            transaction.total_amount = form.cleaned_data["total_amount"]
            transaction.vat_percentage = form.cleaned_data["vat_percentage"]
            transaction.save()
            messages.info(request, f"Transaction {transaction} updated")
            return redirect("pandl")
    else:
        form = EditTransactionForm(
            initial={
                "id": transaction.id,
                "date": transaction.date,
                "label": transaction.label,
                "category": transaction.category,
                "sub_category": transaction.sub_category,
                "total_amount": transaction.total_amount,
                "vat_percentage": transaction.vat_percentage,
            }
        )
    return render(request, "add_transaction.html", {"form": form})
