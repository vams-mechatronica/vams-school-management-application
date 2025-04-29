from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.finance.models import Student, Invoice,AcademicSession,AcademicTerm, StudentClass, InvoiceItem
from datetime import datetime
from django.shortcuts import get_object_or_404

class Command(BaseCommand):
    help = 'Generate fees invoices for all students on the 1st of every month'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        if today.day != 1:
            self.stdout.write("Today is not the 1st. Exiting.")
            return

        students = Student.objects.filter(current_status=1)
        month = today.strftime('%B')
        year = today.year

        for student in students:
            previous_invoice = None
            try:
                previous_invoice = Invoice.objects.get(status=True,student=student,session = AcademicSession.objects.get(current=True),
                term = AcademicTerm.objects.get(current=True),
                month=month,
                class_for = student.current_class)
                if previous_invoice:
                    previous_invoice.status = False
                    previous_invoice.save()
            except Invoice.DoesNotExist:
                pass

            invoice, created = Invoice.objects.get_or_create(
                student=student,
                session = AcademicSession.objects.get(current=True),
                term = AcademicTerm.objects.get(current=True),
                month=month,
                class_for = student.current_class,
                status = True,
                previous_balance = 0
            )
            if previous_invoice and created:
                invoice.previous_balance= previous_invoice.total_payable
            
            if created:
                InvoiceItem.objects.create(invoice=invoice,
                                           class_for=student.current_class,
                                           amount=student.current_class.tuition_fees, description='Tuition Fees')
                InvoiceItem.objects.create(invoice=invoice,
                                           class_for=student.current_class,
                                           amount=student.current_class.computer_fees, description='Computer Fees')
                invoice.total_payable = invoice.balance()
                invoice.save()
                self.stdout.write(f"Invoice created for {student.get_fullname()} for {month} {year}.")
            else:
                self.stdout.write(f"Invoice already exists for {student.get_fullname()} for {month} {year}.")
