# Generated by Django 3.2.5 on 2024-08-07 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_alter_student_registration_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_number',
            field=models.CharField(default='Vedika/2024/0807084642', max_length=200, unique=True),
        ),
    ]
