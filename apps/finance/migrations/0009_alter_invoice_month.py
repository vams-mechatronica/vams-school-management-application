# Generated by Django 4.2.15 on 2024-09-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0008_auto_20240808_1221"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="month",
            field=models.CharField(
                blank=True,
                choices=[
                    ("January", "January"),
                    ("February", "February"),
                    ("March", "March"),
                    ("April", "April"),
                    ("May", "May"),
                    ("June", "June"),
                    ("July", "July"),
                    ("August", "August"),
                    ("September", "September"),
                    ("October", "October"),
                    ("November", "November"),
                    ("December", "December"),
                ],
                default="September",
                max_length=50,
                null=True,
                verbose_name="Month",
            ),
        ),
    ]
