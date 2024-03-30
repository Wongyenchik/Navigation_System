# Generated by Django 5.0.1 on 2024-03-17 02:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0031_productlistitem_location_alter_map_depart_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="map",
            name="depart",
            field=models.CharField(
                choices=[("location1", "Location 1"), ("location2", "Location 2")],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="map",
            name="destination",
            field=models.CharField(
                choices=[("location1", "Location 1"), ("location2", "Location 2")],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("coupler", "Coupler"),
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
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
                    ("coupler", "Coupler"),
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
                    ("clampcylinder", "Clamp Cylinder"),
                ],
                max_length=30,
            ),
        ),
    ]
