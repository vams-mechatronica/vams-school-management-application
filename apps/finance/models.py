# Updated models.py

from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student
from calendar import month_name
from datetime import datetime

def get_current_academic_session():
    return AcademicSession.objects.get(current=True)

def get_current_academic_term():
    return AcademicTerm.objects.get(current=True)



class Invoice(models.Model):
    MONTH_CHOICES = tuple((month_name[i], month_name[i]) for i in range(1, 13))
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True, blank=True,default=get_current_academic_session)
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True,default=get_current_academic_term)
    month = models.CharField(verbose_name="Month", max_length=50, null=True, blank=True, choices=MONTH_CHOICES,default=month_name[datetime.now().month])
    class_for = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        get_latest_by = 'created_at'
    def __str__(self):
        return f"{self.student.firstname} {self.student.surname} - {self.session} /{self.month}"

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


