# Generated by Django 5.0.1 on 2024-02-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0024_alter_user_account_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
                    ("coupler", "Coupler"),
                    ("clampcylinder", "Clamp Cylinder"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="productlistitem",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
                    ("coupler", "Coupler"),
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
                    ("stockpurchaser", "Stock Purchaser"),
                    ("orderpicker", "Order Picker"),
                    ("admin", "Admin"),
                ],
                max_length=30,
            ),
        ),
    ]