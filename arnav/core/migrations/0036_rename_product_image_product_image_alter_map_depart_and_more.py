# Generated by Django 5.0.1 on 2024-03-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0035_product_product_image_alter_product_product_category_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="product_image",
            new_name="image",
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
    ]
