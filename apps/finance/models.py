# Updated models.py

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum
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
    STATUS = [(True, "Active"), (False, "Closed")]
    
    MONTH_CHOICES = tuple((month_name[i], month_name[i]) for i in range(1, 13))
    
    def get_current_month():
        return month_name[datetime.now().month]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True, blank=True, default=get_current_academic_session)
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True, default=get_current_academic_term)
    month = models.CharField(verbose_name="Month", max_length=50, null=True, blank=True, choices=MONTH_CHOICES, default=get_current_month)
    class_for = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.BooleanField(default=True,choices=STATUS)
    is_editable = models.BooleanField(default=True)
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return f"{self.student.firstname} {self.student.surname} - {self.student.registration_number}"

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'pk': self.pk})

    def balance(self):
        return self.total_amount_payable() - self.total_amount_paid()

    def amount_payable(self):
        return InvoiceItem.objects.filter(invoice=self).aggregate(Sum('amount'))['amount__sum'] or 0

    def total_amount_payable(self):
        return self.previous_balance + self.amount_payable()

    def total_amount_paid(self):
        return Receipt.objects.filter(invoice=self).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    def get_status_display(self):
        return "Active" if self.status else "Closed"

    def disable_editing(self):
        """Disable editing if payments have been made or the invoice is older than 30 days"""
        if self.total_amount_paid() > 0 or (now() - self.created_at) > timedelta(days=30):
            self.is_editable = False
            self.save(update_fields=['is_editable'])

    def defaulter_flag(self):
        """
        Yellow/orange/red/critical escalation flag based on days overdue past
        `due_date`, computed on demand rather than stored - mirrors the
        existing disable_editing() pattern of deriving state from due_date/
        balance() rather than persisting a separate status field.
        Returns None if there's no due date, or the invoice isn't overdue
        (fully paid, or due date hasn't passed).
        """
        if not self.due_date or self.balance() <= 0:
            return None
        days_overdue = (timezone.now().date() - self.due_date).days
        if days_overdue > 90:
            return "critical"
        if days_overdue > 60:
            return "red"
        if days_overdue > 30:
            return "orange"
        if days_overdue > 7:
            return "yellow"
        return None

    def save(self, *args, **kwargs):
        """
        - Update `total_payable` before saving.
        - Mark the previous invoice for the same student as non-editable/inactive.
        """
        self.total_payable = self.balance()

        is_new = self.pk is None  
        super().save(*args, **kwargs)  

        if is_new:  
            Invoice.objects.filter(student=self.student, is_editable=True).exclude(pk=self.pk).update(is_editable=False, status=False)



class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name='invoice_items')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    class_for = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def get_absolute_url(self):
        return reverse('invoiceitem-detail', kwargs={'pk': self.pk})

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name='receipts')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50,choices=(('upi','UPI'),('cash','Cash'),('debit-card','Debit Card'),('credit-card','Credit Card'),('net-banking','Net Banking'),('select','Select')),default="select")
    date_paid = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receipt for Invoice {self.invoice} - {self.amount_paid}"


class InvoiceBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="invoice/bulkupload/")


class Concession(models.Model):
    """A fee concession/scholarship granted to a student for a date range.
    Exactly one of `percentage` or `fixed_amount` must be set (validated in
    clean()). Only `verified` concessions active on a given date are applied
    when an invoice is created - see InvoiceSerializer."""

    CONCESSION_TYPES = (
        ("rte", "RTE"),
        ("sibling", "Sibling"),
        ("staff_ward", "Staff Ward"),
        ("merit", "Merit Scholarship"),
        ("govt_scholarship", "Govt. Scholarship"),
        ("ews", "EWS"),
        ("differently_abled", "Differently Abled"),
        ("discretionary", "Management Discretionary"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="concessions")
    concession_type = models.CharField(max_length=30, choices=CONCESSION_TYPES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    approval_date = models.DateField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_concession_type_display()} - {self.student}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if bool(self.percentage) == bool(self.fixed_amount):
            raise ValidationError(
                "Exactly one of percentage or fixed_amount must be set."
            )

    def is_active_on(self, date):
        return self.verified and self.valid_from <= date <= self.valid_to

    def discount_amount(self, base_amount):
        base_amount = Decimal(base_amount)
        if self.percentage:
            return (base_amount * self.percentage) / Decimal("100")
        return self.fixed_amount or Decimal("0.00")