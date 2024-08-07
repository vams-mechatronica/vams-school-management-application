
from django.forms import inlineformset_factory, modelformset_factory,ModelForm
from .models import Invoice, InvoiceItem, Receipt

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"

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

# # Writing the updated content back to the files
# with open(models_path, 'w') as models_file:
#     models_file.write(updated_models_content)

# with open(views_path, 'w') as views_file:
#     views_file.write(updated_views_content)

# with open(forms_path, 'w') as forms_file:
#     forms_file.write(updated_forms_content)

# (models_path, views_path, forms_path)
