# Generated by Django 3.2.5 on 2024-08-07 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20240807_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_number',
            field=models.CharField(default='Vedika/2024/0807074655', max_length=200, unique=True),
        ),
    ]
