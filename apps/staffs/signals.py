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
import pandas as pd


@receiver(post_save, sender=StaffBulkUpload)
def create_bulk_staff(sender, instance, created, *args, **kwargs):
    if not created:
        return
    
    staff = []
    timestamp = timezone.now().strftime('%d')
    ext = os.path.splitext(instance.csv_file.name)[1].lower()
    
    with transaction.atomic():  # Ensures database integrity in case of failure
        if ext == ".csv":
            opened = StringIO(instance.csv_file.read().decode())
            reading = csv.DictReader(opened, delimiter=",")
        elif ext == ".xlsx":
            df = pd.read_excel(instance.csv_file)
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            reading = df.to_dict(orient="records")
        
        column_mapping = {
            "emp_code": "emp_code",
            "surname": "surname",
            "first_name": "firstname",
            "other_names": "other_names",
            "gender": "gender",
            "mobile_number": "mobile_number",
            "address": "address",
            "adhar_card_number": "adhar_card_number"
        }
        
        for counter, row in enumerate(reading, start=1):
            normalized_row = {column_mapping.get(k.strip().lower().replace(" ", "_"), k.strip().lower().replace(" ", "_")): v for k, v in row.items()}
            
            reg = normalized_row.get("emp_code") or f"SLN/EMP/{timezone.now().year}/{timestamp}{counter}"
            surname = normalized_row.get("surname", "-")
            firstname = normalized_row.get("firstname", None)
            other_names = normalized_row.get("other_names", "-")
            gender = str(normalized_row.get("gender", "")).lower()
            phone = normalized_row.get("mobile_number", "")
            address = normalized_row.get("address", "")
            adhar_card_number = normalized_row.get("adhar_card_number", "")

            if not firstname:
                firstname = surname

            staff.append(
                Staff(
                    emp_code=reg,
                    surname=surname,
                    firstname=firstname,
                    other_name=other_names,
                    gender=gender,
                    mobile_number=phone,
                    address=address,
                    adhar_card_number=adhar_card_number,
                    current_status=1,
                )
            )
        
        Staff.objects.bulk_create(staff, ignore_conflicts=True)
    
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


# @receiver(post_delete, sender=Staff)
# def delete_passport_on_delete(sender, instance, *args, **kwargs):
#     if instance.adharcard:
#         _delete_file(instance.adharcard.path)
