# Updated models.py

from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student
from calendar import month_name

class Invoice(models.Model):
    MONTH_CHOICES = tuple((str(i), month_name[i]) for i in range(1, 13))
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True, blank=True)
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True)
    month = models.CharField(verbose_name="Month", max_length=50, null=True, blank=True, choices=MONTH_CHOICES)
    class_for = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    balance_from_previous_term = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.firstname} {self.student.surname} - {self.session} /{self.month}"

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'pk': self.pk})

    def add_monthly_tuition_fee(self):
        # Assuming tuition fee is stored in the StudentClass model
        tuition_fee = self.class_for.tuition_fee
        InvoiceItem.objects.create(
            invoice=self,
            description='Monthly Tuition Fee',
            amount=tuition_fee
        )
    
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
        return self.balance_from_previous_term + self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount_paid
        return amount


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
    date_paid = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receipt for Invoice {self.invoice} - {self.amount_paid}"


