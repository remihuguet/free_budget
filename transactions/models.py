from django.db import models
from django.forms import ValidationError

CATEGORIES = [
    (0, "Non catégorisé"),
    (1, "Revenus"),
    (2, "Dépenses fixes"),
    (3, "Salaires"),
    (4, "Dividendes"),
    (5, "Cotisations"),
    (6, "Taxe et impôts"),
    (7, "Autres"),
]


class SubCategory(models.Model):
    name = models.CharField(max_length=1000)
    category = models.IntegerField(choices=CATEGORIES)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_percentage = models.IntegerField(
        default=0,
    )
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.IntegerField(choices=CATEGORIES)
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transactions",
    )
    label = models.CharField(max_length=1000)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.sub_category and self.sub_category.category != self.category:
            raise ValidationError("Sub category must be in the same category")

    @property
    def total_amount(self):
        return self.amount + self.vat_amount
