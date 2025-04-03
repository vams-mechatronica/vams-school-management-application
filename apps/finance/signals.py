from django.db.models.signals import post_save
from django.dispatch import receiver

import csv
import os
from io import StringIO
from django.utils import timezone
from django.db import transaction
from .models import Invoice,InvoiceItem, InvoiceBulkUpload, Student, StudentClass, AcademicSession, AcademicTerm,Receipt


@receiver(post_save, sender=Invoice)
def after_creating_invoice(sender, instance, created, **kwargs):
    if created:
        instance.total_payable = instance.balance()
        instance.save
        previous_inv = (
            Invoice.objects.filter(student=instance.student)
            .exclude(id=instance.id)
            .last()
        )
        if previous_inv:
            previous_inv.status = False
            previous_inv.save()
            instance.balance_from_previous_term = previous_inv.balance()
            instance.save()

@receiver(post_save,sender=Receipt)
def after_creating_new_receipt(sender, instance,created, **kwargs):
    if created:
        invoice = instance.invoice  
        if invoice:  
            invoice.total_payable = invoice.balance()
            invoice.disable_editing()
            invoice.save(update_fields=['total_payable', 'is_editable','updated_at'])


from decimal import Decimal, InvalidOperation

@receiver(post_save, sender=InvoiceBulkUpload)
def create_bulk_student(sender, instance, created, *args, **kwargs):
    if not created:
        return

    # Read the uploaded CSV file
    opened = StringIO(instance.csv_file.read().decode())
    reading = csv.DictReader(opened, delimiter=",")

    with transaction.atomic():
        for counter, row in enumerate(reading, start=1):
            reg = row.get("registration_number")
            fee_for_month = row.get("fees_for_month")
            previous_balance = row.get("previous_balance")

            # Get Student
            try:
                student = Student.objects.get(registration_number=reg)
            except Student.DoesNotExist:
                continue  # Skip if student is not found

            classi = student.current_class
            term = AcademicTerm.objects.get(current=True)
            session = AcademicSession.objects.get(current=True)

            # Extract fee fields dynamically
            standard_fees = ["tuition_fee", "computer_fee", "admission_fee", "exam_fee", "miscellaneous"]
            fee_items = {}

            for key in standard_fees:
                value = row.get(key, "0.00")
                try:
                    fee_items[key] = Decimal(value)  # Convert to Decimal
                except (InvalidOperation, TypeError, ValueError):
                    fee_items[key] = Decimal("0.00")  # Default to 0.00 if invalid

            # Identify additional fee columns dynamically
            extra_fees = {}
            for key, value in row.items():
                if key not in ["registration_number", "fees_for_month", "previous_balance","student_name"] and key not in standard_fees:
                    try:
                        extra_fees[key] = Decimal(value)
                    except (InvalidOperation, TypeError, ValueError):
                        extra_fees[key] = Decimal("0.00")  # Default invalid values to 0.00

            # Save or Update Invoice
            invoice, created = Invoice.objects.update_or_create(
                student=student,
                session=session,
                term=term,
                month=fee_for_month,
                class_for=classi,
                status=True,
                defaults={"previous_balance": previous_balance}
            )

            # Prepare Invoice Items
            invoice_items = []

            # Standard Fees
            for description, amount in fee_items.items():
                invoice_items.append(InvoiceItem(invoice=invoice, class_for=classi, description=description.replace("_", " ").title(), amount=amount))

            # Additional Fees from CSV
            for description, amount in extra_fees.items():
                invoice_items.append(InvoiceItem(invoice=invoice, class_for=classi, description=description.replace("_", " ").title(), amount=amount))

            if invoice_items:
                if created:
                    InvoiceItem.objects.bulk_create(invoice_items, ignore_conflicts=True)
                else:
                    for item in invoice_items:
                        InvoiceItem.objects.update_or_create(
                            invoice=invoice,
                            class_for=classi,
                            description=item.description,
                            defaults={"amount": item.amount}
                        )

    instance.csv_file.close()
    instance.delete()
