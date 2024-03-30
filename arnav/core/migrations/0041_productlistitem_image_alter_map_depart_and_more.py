# Generated by Django 5.0.1 on 2024-03-22 07:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0040_alter_map_depart_alter_map_destination_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productlistitem",
            name="image",
            field=models.ImageField(default=1, upload_to="product"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="map",
            name="depart",
            field=models.CharField(
                choices=[("location2", "Location 2"), ("location1", "Location 1")],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="map",
            name="destination",
            field=models.CharField(
                choices=[("location2", "Location 2"), ("location1", "Location 1")],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="product"),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("coupler", "Coupler"),
                    ("nylontubing", "Nylon Tubing"),
                    ("clampcylinder", "Clamp Cylinder"),
                    ("silencer", "Silencer"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="productlistitem",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("coupler", "Coupler"),
                    ("nylontubing", "Nylon Tubing"),
                    ("clampcylinder", "Clamp Cylinder"),
                    ("silencer", "Silencer"),
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
                    ("stockpurchaser", "Stock Purchaser"),
                    ("orderpicker", "Order Picker"),
                ],
                max_length=30,
            ),
        ),
    ]