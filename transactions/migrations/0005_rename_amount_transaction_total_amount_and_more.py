# Generated by Django 4.0.4 on 2022-05-22 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_remove_transaction_total_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='amount',
            new_name='total_amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='vat_amount',
        ),
    ]
