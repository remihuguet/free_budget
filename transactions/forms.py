from . import models
from django import forms


class AddTransactionForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget())
    label = forms.CharField(label="Description", max_length=1000)
    category = forms.ChoiceField(choices=models.CATEGORIES, label="Catégorie")
    sub_category = forms.ModelChoiceField(models.SubCategory.objects, required=False)
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    vat_percentage = forms.ChoiceField(
        choices=((0, "0"), (5, "5%"), (10, "10%"), (20, "20%"))
    )

    def is_valid(self) -> bool:
        is_valid = super().is_valid()
        if self.cleaned_data["sub_category"] and int(
            self.cleaned_data["sub_category"].category
        ) != int(self.cleaned_data["category"]):
            self.add_error(
                "sub_category",
                forms.ValidationError(
                    "Sub category must be of the same category that the transaction"
                ),
            )
            return False
        return is_valid


class EditTransactionForm(AddTransactionForm):
    id = forms.IntegerField()
