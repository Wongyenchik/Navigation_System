# Generated by Django 5.0.1 on 2024-02-16 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_alter_map_depart_alter_map_destination_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="map",
            name="depart",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
