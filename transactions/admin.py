from django.contrib import admin
from .models import Transaction, SubCategory


class TransactionInline(admin.TabularInline):
    model = Transaction


class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]


class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    exclude = []
    fieldsets = (
        (None, {"fields": ("date", "total_amount", "category", "label")}),
        ("Détails", {"fields": ("sub_category", "vat_percentage")}),
    )
    list_display = ("id", "date", "total_amount", "amount", "label", "category")
    list_filter = ("date", "category")
    list_editable = ("date", "category", "label", "total_amount")
    ordering = ("-date",)
    search_fields = ("label", "amount")


# Register your models here.

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
