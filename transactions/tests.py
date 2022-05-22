import decimal
import pytest
from transactions.models import Transaction, SubCategory
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_transaction_sub_category_must_have_same_category():
    s = SubCategory(name="test", category=1)
    t = Transaction(
        total_amount=100,
        label="Test",
        category=0,
        sub_category=s,
    )
    with pytest.raises(ValidationError):
        t.save()


@pytest.mark.django_db
def test_transaction_saved_correctly():
    s = SubCategory(name="test", category=1)
    s.save()
    t = Transaction(
        total_amount=100,
        vat_percentage=20,
        label="Test",
        category=1,
        sub_category=s,
    )
    t.save()

    saved = Transaction.objects.get(label="Test")
    assert saved == t
    assert saved.amount == decimal.Decimal("83.33")
    assert saved.vat_amount == decimal.Decimal("16.67")
