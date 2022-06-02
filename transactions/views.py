from typing import Any, Dict
from django.contrib import messages
from django.shortcuts import get_object_or_404, resolve_url
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from transactions.forms import AddTransactionForm, EditTransactionForm
from .models import SubCategory, Transaction


class ProfitsAndLossesView(TemplateView):
    template_name: str = "profits_and_losses.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

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
            ] = (
                transac.total_amount,
                resolve_url(to="edit_transaction", id=transac.id),
            )
        ctx["months"] = months
        ctx["ref_months"] = ref_months
        ctx["pandl"] = p_and_l
        return ctx


class TransactionForm(FormView):
    template_name = "add_transaction.html"
    form_class = AddTransactionForm
    success_url = "/transactions/pl"

    def form_valid(self, form):
        transaction = Transaction(**form.cleaned_data)
        transaction.category = int(form.cleaned_data["category"])
        transaction.save()
        messages.info(self.request, f"Transaction {transaction} created")
        return super().form_valid(form)


class EditTransactionForm(FormView):
    template_name = "add_transaction.html"
    form_class = EditTransactionForm
    success_url = "/transactions/pl"

    def dispatch(self, request, *args: Any, **kwargs: Any):
        self.transaction = get_object_or_404(Transaction.objects, id=kwargs["id"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self) -> Dict[str, Any]:
        return {
            "id": self.transaction.id,
            "date": self.transaction.date,
            "label": self.transaction.label,
            "category": self.transaction.category,
            "sub_category": self.transaction.sub_category,
            "total_amount": self.transaction.total_amount,
            "vat_percentage": self.transaction.vat_percentage,
        }

    def form_valid(self, form):
        Transaction.objects.filter(id=self.transaction.id).update(**form.cleaned_data)
        messages.info(self.request, f"Transaction {self.transaction} updated")
        return super().form_valid(form)


class SubCategoriesView(ListView):
    model = SubCategory
    template_name = "subcategory_list.html"


class SubCategoryMixin:
    model = SubCategory
    fields = ["name", "category"]
    success_url = "/transactions/subcategories"
    template_name = "subcategory_create.html"


class AddSubCategoryView(SubCategoryMixin, CreateView):
    pass


class UpdateSubCategoryView(SubCategoryMixin, UpdateView):
    pass


class DeleteSubCategoryView(SubCategoryMixin, DeleteView):
    template_name = "subcategory_delete.html"
