# Updated models.py

from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.timezone import now
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student
from calendar import month_name
from datetime import datetime

def get_current_academic_session():
    return AcademicSession.objects.get(current=True)

def get_current_academic_term():
    return AcademicTerm.objects.get(current=True)


class Invoice(models.Model):
    STATUS = [(1, "Active"), (0, "Closed")]
    MONTH_CHOICES = tuple((month_name[i], month_name[i]) for i in range(1, 13))
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True, blank=True,default=get_current_academic_session)
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True,default=get_current_academic_term)
    month = models.CharField(verbose_name="Month", max_length=50, null=True, blank=True, choices=MONTH_CHOICES,default=month_name[datetime.now().month])
    class_for = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    status = models.BooleanField(default=1,choices=STATUS)
    # New field to control editing
    is_editable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        get_latest_by = 'created_at'
    
    def __str__(self):
        return f"{self.student.firstname} {self.student.surname} - {self.student.registration_number}"

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'pk': self.pk})

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()
        return payable - paid

    def amount_payable(self):
        items = InvoiceItem.objects.filter(invoice=self)
        total = 0
        for item in items:
            total += item.amount
        return total

    def total_amount_payable(self):
        return self.previous_balance + self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount_paid
        return amount
    
    def disable_editing(self):
        """Disable editing if payments have been made or the invoice is older than 30 days"""
        if self.total_amount_paid() > 0 or (now() - self.created_at) > timedelta(days=30):
            self.is_editable = False
            self.save()
    
    def save(self, *args, **kwargs):
        """
        When a new invoice is created, mark the previous invoice for the same student as non-editable.
        """
        if self.pk is None:  # Only execute this check for new invoices
            previous_invoice = Invoice.objects.filter(student=self.student).order_by('-updated_at')
            for inv in previous_invoice:
                if inv:
                    inv.is_editable = False
                    inv.save(update_fields=['is_editable'])

        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    class_for = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def get_absolute_url(self):
        return reverse('invoiceitem-detail', kwargs={'pk': self.pk})

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50,choices=(('upi','UPI'),('cash','Cash'),('debit-card','Debit Card'),('credit-card','Credit Card'),('net-banking','Net Banking'),('select','Select')),default="select")
    date_paid = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receipt for Invoice {self.invoice} - {self.amount_paid}"


class InvoiceBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="invoice/bulkupload/")