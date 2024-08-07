
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone
from django.forms import widgets

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.students.models import Student
from apps.corecode.models import StudentClass


from apps.students.models import Student
from .forms import InvoiceItemFormset, InvoiceReceiptFormSet, Invoices
from .models import Invoice, InvoiceItem, Receipt
from apps.result.utils import PermissionRequiredMessageMixin, has_permission

class InvoiceListView(LoginRequiredMixin,PermissionRequiredMessageMixin, ListView):
    model = Invoice
    permission_required = "finance.view_invoice"

class InvoiceCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, CreateView):
    model = Invoice
    fields = "__all__"
    permission_required = "finance.add_invoice"
    success_url = "/finance/list"

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = InvoiceItemFormset(
                self.request.POST, prefix="invoiceitem_set"
            )
        else:
            context["items"] = InvoiceItemFormset(prefix="invoiceitem_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)

@has_permission('finance.add_invoice')
@login_required
def generate_monthly_invoices(request):
    current_month = timezone.now().month
    for student in Student.objects.all():
        if not Invoice.objects.filter(student=student, month=str(current_month)).exists():
            invoice = Invoice.objects.create(
                student=student,
                session=student.session,
                term=student.term,
                month=str(current_month),
                class_for=student.student_class
            )
            invoice.add_monthly_tuition_fee()
    return redirect('invoice-list')

class InvoiceDetailView(LoginRequiredMixin, PermissionRequiredMessageMixin,DetailView):
    model = Invoice
    permission_required = "finance.view_invoice"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context["receipts"] = Receipt.objects.filter(invoice=self.object)
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
        return context


class InvoiceUpdateView(LoginRequiredMixin,PermissionRequiredMessageMixin, UpdateView):
    model = Invoice
    permission_required = "finance.update_invoice"
    fields = ["student", "session", "term","month", "class_for", "previous_balance"]

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            context["items"] = InvoiceItemFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)
            context["items"] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["receipts"]
        itemsformset = context["items"]
        if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
            form.save()
            formset.save()
            itemsformset.save()
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    model = Invoice
    permission_required = "finance.delete_invoice"
    success_url = reverse_lazy("invoice-list")


class ReceiptCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, CreateView):
    model = Receipt
    permission_required = "finance.add_receipt"
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")
    def get_form(self):
        """add date picker in forms"""
        form = super(ReceiptCreateView, self).get_form()
        form.fields["date_paid"].widget = widgets.DateTimeInput(attrs={"type": "date"})
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("invoice-list")

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin,PermissionRequiredMessageMixin,UpdateView):
    model = Receipt
    permission_required = "finance.update_receipt"
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")


class ReceiptDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    model = Receipt
    permission_required = "finance.delete_receipt"
    success_url = reverse_lazy("invoice-list")


@login_required
def bulk_invoice(request):
    return render(request, "finance/bulk_invoice.html")


@has_permission('finance.add_invoice')
@require_GET
def get_student_data(request):
    student_id = request.GET.get('student_id')
    if student_id:
        try:
            student = Student.objects.get(pk=student_id)
            try:
                invoice = Invoice.objects.filter(student=student.pk).latest()
            except Invoice.DoesNotExist:
                invoice = None
            student_class = student.current_class

            # Prepare description-amount dictionary
            item_data = [{'description':'Tuition Fees','amount': student_class.tuition_fees},{'description':'Computer Fees','amount': student_class.computer_fees},{'description':'Admission Fees','amount': student_class.admission_fees},{'description':'Exam Fees','amount': student_class.exam_fees},{'description':'Miscellaneous','amount': student_class.miscellaneous}]
            
            data = {
                'class_for': student.current_class.pk if student.current_class else None,
                'balance_from_previous_term': invoice.balance() if invoice else 0,
                'items': item_data,
            }
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'No student ID provided'}, status=400)
