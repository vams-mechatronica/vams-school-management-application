# Generated by Django 3.2.5 on 2024-08-08 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_alter_student_registration_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_number',
            field=models.CharField(default='Vedika/2024/0808122000', max_length=200, unique=True),
        ),
    ]
