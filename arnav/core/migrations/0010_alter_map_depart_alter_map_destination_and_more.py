# Generated by Django 5.0.1 on 2024-02-16 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_map_alter_product_product_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="map",
            name="depart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="departures",
                to="core.product",
            ),
        ),
        migrations.AlterField(
            model_name="map",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="destinations",
                to="core.product",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("silencer", "Silencer"),
                    ("coupler", "Coupler"),
                    ("nylontubing", "Nylon Tubing"),
                    ("clampcylinder", "Clamp Cylinder"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="account_type",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("orderpicker", "Order Picker"),
                    ("stockpurchaser", "Stock Purchaser"),
                ],
                max_length=30,
            ),
        ),
    ]