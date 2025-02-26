
from django.forms import inlineformset_factory, modelformset_factory,ModelForm,ModelChoiceField
from django_select2.forms import Select2Widget,ModelSelect2Widget
from .models import Invoice, InvoiceItem, Receipt, Student

class StudentSelect2Widget(ModelSelect2Widget):
    model = Student
    search_fields = ["firstname__icontains", "surname__icontains", "admission_number__icontains"]   


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        widgets = {
            'student': StudentSelect2Widget
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(InvoiceForm, self).__init__(*args, **kwargs)
        if student:
            self.fields['class_for'].initial = student.student_class
            self.fields['session'].initial = student.session
            self.fields['term'].initial = student.term

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=["description", "amount"], extra=1, can_delete=True
)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice,
    Receipt,
    fields=("amount_paid", "date_paid", "comment"),
    extra=0,
    can_delete=True,
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)

