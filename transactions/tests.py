from unicodedata import category
from transactions.models import Transaction, SubCategory
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
def test_transaction_sub_category_must_have_same_category():
    s = SubCategory(name="test", category=1)
    t = Transaction(
        amount=100,
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
        amount=100,
        label="Test",
        category=1,
        sub_category=s,
    )
    t.save()

    saved = Transaction.objects.get(label="Test")
    assert saved == t
    assert saved.total_amount == 100
