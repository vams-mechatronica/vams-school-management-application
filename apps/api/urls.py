from django.urls import path,include
from .views import *
urlpatterns = [
    path('app-version',APKVersionAPI.as_view()),

    path('account/',include('dj_rest_auth.urls')),
    path('account/registration/', include('dj_rest_auth.registration.urls')),
    path('student/get/',StudentAPI.as_view()),
    path('student/create/',StudentCreateAPI.as_view()),
    path('student/detail/', StudentDetailAPI.as_view(), name='student-detail'),
    path('student/update/<int:pk>/', StudentUpdateAPI.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', StudentDeleteAPI.as_view(), name='student-delete'),
    # path(''),

    #staff
    path('staff/get/', StaffListAPI.as_view(), name='staff-list'),
    path('staff/create/', StaffCreateAPI.as_view(), name='staff-create'),
    path('staff/<int:pk>/', StaffRetrieveUpdateDestroyView.as_view(), name='staff-retrieve-update-destroy'),


    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),

    # AcademicSession URLs
    path('academic-sessions/', AcademicSessionListCreateView.as_view(), name='academic-session-list-create'),
    path('academic-sessions/<int:pk>/', AcademicSessionRetrieveUpdateDestroyView.as_view(), name='academic-session-retrieve-update-destroy'),

    # AcademicTerm URLs
    path('academic-terms/', AcademicTermListCreateView.as_view(), name='academic-term-list-create'),
    path('academic-terms/<int:pk>/', AcademicTermRetrieveUpdateDestroyView.as_view(), name='academic-term-retrieve-update-destroy'),

    # StudentClass URLs
    path('student-classes/', StudentClassListCreateView.as_view(), name='student-class-list-create'),
    path('student-classes/<int:pk>/', StudentClassRetrieveUpdateDestroyView.as_view(), name='student-class-retrieve-update-destroy'),

    # Receipt URLs
    path('receipts/', ReceiptListCreateView.as_view(), name='receipt-list-create'),
    path('receipts/<int:pk>/', ReceiptRetrieveUpdateDestroyView.as_view(), name='receipt-retrieve-update-destroy'),

    path('schools/', SchoolListAPI.as_view(), name='school-list'),
    path('schools/create/', SchoolCreateAPI.as_view(), name='school-create'),
    path('schools/<int:pk>/', SchoolRetrieveAPI.as_view(), name='school-detail'),
    path('schools/<int:pk>/update/', SchoolUpdateAPI.as_view(), name='school-update'),
    path('schools/<int:pk>/delete/', SchoolDeleteAPI.as_view(), name='school-delete'),
]
