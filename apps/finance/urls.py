from django.urls import path

from .views import (
    InvoiceCreateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
    InvoiceUpdateView,
    ReceiptCreateView,
    ReceiptUpdateView,
    bulk_invoice,
    get_student_data,
    DownloadCSVView,
    InvoiceBulkUploadView
)

urlpatterns = [
    path("list/", InvoiceListView.as_view(), name="invoice-list"),
    path("create/", InvoiceCreateView.as_view(), name="invoice-create"),
    path("<int:pk>/detail/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("<int:pk>/update/", InvoiceUpdateView.as_view(), name="invoice-update"),
    path("<int:pk>/delete/", InvoiceDeleteView.as_view(), name="invoice-delete"),
    path("receipt/create", ReceiptCreateView.as_view(), name="receipt-create"),
    path(
        "receipt/<int:pk>/update/", ReceiptUpdateView.as_view(), name="receipt-update"
    ),
    path("bulk-invoice/", InvoiceBulkUploadView.as_view(), name="bulk-invoice"),
    path('create/api/get-student-data/', get_student_data, name='get-student-data'),
    path("download-csv",DownloadCSVView.as_view(),name="download-csv-invoice"),
]
