# Generated by Django 5.0.1 on 2024-02-17 16:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_alter_product_product_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productlistitem",
            name="stock",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("clampcylinder", "Clamp Cylinder"),
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
                    ("coupler", "Coupler"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="productlistitem",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("clampcylinder", "Clamp Cylinder"),
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
                    ("coupler", "Coupler"),
                ],
                max_length=30,
            ),
        ),
    ]
