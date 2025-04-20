import csv
import os
from io import StringIO
from django.utils import timezone
import pandas as pd
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from datetime import datetime

from apps.corecode.models import StudentClass
from django.db import transaction
from .models import Student, StudentBulkUpload
from apps.corecode.models import SchoolDetail


@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, instance, created, *args, **kwargs):
    if not created:
        return
    
    students = []
    timestamp = timezone.now().strftime('%d')
    ext = os.path.splitext(instance.csv_file.name)[1].lower()
    try:
        last_id = Student.objects.latest('created_at').id
    except Student.DoesNotExist:
        last_id = 0
    
    try:
        registration_prefix = SchoolDetail.objects.latest('updated_at').short_name
    except SchoolDetail.DoesNotExist:
        registration_prefix = "VAMS"
    
    with transaction.atomic():  # Ensures database integrity in case of failure
        if ext == ".csv":
            opened = StringIO(instance.csv_file.read().decode())
            reading = csv.DictReader(opened, delimiter=",")
        elif ext == ".xlsx":
            df = pd.read_excel(instance.csv_file)
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            reading = df.to_dict(orient="records")
        
        column_mapping = {
            "registration_number": "registration_number",
            "student_name": "student_name",
            "gender": "gender",
            "father_name": "father_name",
            "mother_name": "mother_name",
            "mobile_number": "parent_mobile_number",
            "address": "address",
            "current_class": "current_class",
            "date_of_birth":"date_of_birth"
        }
        
        for counter, row in enumerate(reading, start=1):
            counter += last_id
            normalized_row = {column_mapping.get(k.strip().lower().replace(" ", "_"), k.strip().lower().replace(" ", "_")): v for k, v in row.items()}
            
            reg = normalized_row.get("registration_number") or f"{registration_prefix}/{timezone.now().year}/{timezone.now().month}/{timestamp}/{counter}"
            student_name = normalized_row.get("student_name", "")
            other_names = normalized_row.get("other_names", "")
            gender = str(normalized_row.get("gender", "")).lower()
            father_name = normalized_row.get("father_name", "")
            mother_name = normalized_row.get("mother_name", "")
            phone = normalized_row.get("parent_mobile_number", "")
            address = normalized_row.get("address", "")
            current_class_name = normalized_row.get("current_class", "")
            dob = normalized_row.get("date_of_birth",None)

            # Handle DOB conversion with multiple formats
            dob = normalized_row.get("dob", "")
            if dob:
                try:
                    dob = datetime.strptime(dob, "%d/%m/%Y")
                except ValueError:
                    try:
                        dob = datetime.strptime(dob, "%Y-%m-%d")
                    except ValueError:
                        dob = timezone.now()
            else:
                dob = timezone.now()
            
            first_name = ""
            sur_name = ""
            if student_name:
                sname = student_name.split(' ')
                if len(sname) > 1:
                    first_name = sname[0]
                    sur_name = sname[1]
                elif len(sname) == 1:
                    first_name = sname[0]
                    sur_name = ""

            # Fetch or create class
            theclass = None
            if current_class_name:
                theclass, _ = StudentClass.objects.get_or_create(name=current_class_name)

            students.append(
                Student(
                    registration_number=reg,
                    surname=sur_name,
                    firstname=first_name,
                    other_name=other_names,
                    gender=gender,
                    father_name=father_name,
                    mother_name=mother_name,
                    current_class=theclass,
                    parent_mobile_number=phone,
                    address=address,
                    current_status=1,
                    date_of_birth = dob,
                )
            )

        # Bulk insert students (avoiding duplicate checks in loop)
        Student.objects.bulk_create(students,ignore_conflicts=True)
        # Student.objects.bulk_create(students, update_conflicts=True,unique_fields=['registration_number'],update_fields=['updated_at'])

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
