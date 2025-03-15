import csv
import os
from io import StringIO
from django.utils import timezone

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.corecode.models import StudentClass
from django.db import transaction
from .models import Student, StudentBulkUpload


@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, instance, created, *args, **kwargs):
    if not created:
        return
    
    # Read the uploaded CSV file
    opened = StringIO(instance.csv_file.read().decode())
    reading = csv.DictReader(opened, delimiter=",")

    students = []
    timestamp = timezone.now().strftime('%d')
    
    with transaction.atomic():  # Ensures database integrity in case of failure
        for counter, row in enumerate(reading, start=1):
            reg = row.get("registration_number") or f"SLN/{timezone.now().year}/{timezone.now().month}/{timestamp}/{counter}"
            surname = row.get("surname", "")
            firstname = row.get("firstname", "")
            other_names = row.get("other_names", "")
            gender = row.get("gender", "").lower()
            father_name = row.get("father_name", "")
            mother_name = row.get("mother_name", "")
            phone = row.get("parent_number", "")
            address = row.get("address", "")
            current_class_name = row.get("current_class", "")

            # Fetch or create class
            theclass = None
            if current_class_name:
                theclass, _ = StudentClass.objects.get_or_create(name=current_class_name)

            students.append(
                Student(
                    registration_number=reg,
                    surname=surname,
                    firstname=firstname,
                    other_name=other_names,
                    gender=gender,
                    father_name=father_name,
                    mother_name=mother_name,
                    current_class=theclass,
                    parent_mobile_number=phone,
                    address=address,
                    current_status=1,
                )
            )

        # Bulk insert students (avoiding duplicate checks in loop)
        Student.objects.bulk_create(students, ignore_conflicts=True)  # Ignores duplicates if constraints exist

    instance.csv_file.close()
    instance.delete()

def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=StudentBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Student)
def delete_passport_on_delete(sender, instance, *args, **kwargs):
    if instance.adharcard:
        _delete_file(instance.adharcard.path)
