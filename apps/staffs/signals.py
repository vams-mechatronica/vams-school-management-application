import csv
import os
from io import StringIO
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.corecode.models import StudentClass
from django.db import transaction
from .models import Staff,StaffBulkUpload


@receiver(post_save, sender=StaffBulkUpload)
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
            reg = row.get("emp_code") or f"SLN/EMP/{timezone.now().year}/{timestamp}{counter}"
            surname = row.get("surname", "")
            firstname = row.get("firstname", "")
            other_names = row.get("other_names", "")
            gender = row.get("gender", "").lower()
            phone = row.get("mobile_number", "")
            address = row.get("address", "")
            date_of_birth = row.get("address", "")
            date_of_joining = row.get("address", "")
            adhar_card_number = row.get("adhar_card_number", "")

            date_of_birth = datetime.strptime(date_of_birth,'%Y-%m-%d')
            date_of_joining = datetime.strptime(date_of_joining,'%Y-%m-%d')

            students.append(
                Staff(
                    registration_number=reg,
                    surname=surname,
                    firstname=firstname,
                    other_name=other_names,
                    gender=gender,
                    mobile_number=phone,
                    address=address,
                    date_of_birth=date_of_birth,
                    date_of_joining=date_of_joining,
                    adhar_card_number=adhar_card_number,
                    current_status="active",
                )
            )

        # Bulk insert students (avoiding duplicate checks in loop)
        Staff.objects.bulk_create(students, ignore_conflicts=True)  # Ignores duplicates if constraints exist

    instance.csv_file.close()
    instance.delete()

def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=StaffBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Staff)
def delete_passport_on_delete(sender, instance, *args, **kwargs):
    if instance.adharcard:
        _delete_file(instance.adharcard.path)
