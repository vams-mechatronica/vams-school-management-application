# Generated by Django 3.2.5 on 2024-08-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20201124_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='passport',
        ),
        migrations.AddField(
            model_name='student',
            name='adharcard',
            field=models.ImageField(blank=True, upload_to='students/adharcard/'),
        ),
    ]
