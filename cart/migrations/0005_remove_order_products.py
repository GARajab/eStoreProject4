# Generated by Django 5.1.5 on 2025-02-18 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]
