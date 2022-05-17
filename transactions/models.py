from django.db import models

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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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
