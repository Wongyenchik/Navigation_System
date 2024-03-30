# Generated by Django 5.0.1 on 2024-02-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_alter_map_depart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="map",
            name="depart",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("clampcylinder", "Clamp Cylinder"),
                    ("coupler", "Coupler"),
                    ("nylontubing", "Nylon Tubing"),
                    ("silencer", "Silencer"),
                ],
                max_length=30,
            ),
        ),
    ]