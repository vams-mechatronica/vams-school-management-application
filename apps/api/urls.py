from django.urls import path,include
from .views import *

urlpatterns = [
    path('app-version',APKVersionAPI.as_view()),
    path('error-log/',ErrorLogAPI.as_view()),
    path('users/',UsersAPI.as_view()),
    path('dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard-data-api'),
    path('account/',include('dj_rest_auth.urls')),
    path('account/registration/', include('dj_rest_auth.registration.urls')),
    path('user/profile/',UserProfile.as_view()),
    path('user/profile/auth/',UserProfileU.as_view()),
    path('student/get/',StudentAPI.as_view()),
    path('student/create/',StudentCreateAPI.as_view()),
    path('student/create/bulk/',StudentBulkUploadAPI.as_view()),
    path('student/detail/', StudentDetailAPI.as_view(), name='student-detail'),
    path('student/update/<int:pk>/', StudentUpdateAPI.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', StudentDeleteAPI.as_view(), name='student-delete'),
    path('student/attendance/',StudentAttendanceAPI.as_view(),name="student-attendance-api"),

    #staff
    path('staff/get/', StaffListAPI.as_view(), name='staff-list'),
    path('staff/create/', StaffCreateAPI.as_view(), name='staff-create'),
    path('staff/create/bulk/',StaffBulkUploadAPI.as_view()),
    path('staff/<int:pk>/', StaffRetrieveUpdateDestroyView.as_view(), name='staff-retrieve-update-destroy'),
    path('staff/attendance/',StaffAttendenceAPI.as_view(),name="staff-attendance-api"),
    path('staff/attendance/record-time/',StaffAttendanceView.as_view(),name="staff-attendance-time-record"),


    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/set/', InvoiceViewSet.as_view({'get': 'list', 'post': 'create'}), name="invoice-list"),
    path('invoices/set/<int:pk>/', InvoiceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="invoice-detail"),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),
    path('invoice/detail/',InvoiceDetailAPI.as_view()),

    # Results 
    path('results/',StudentResultView.as_view()),

    # Notifications
    path('notifications/',NotificationListAPI.as_view()),
    path('notification/mark-as-read/',NotificationMarkAsReadAPI.as_view()),

    # AcademicSession URLs
    path('academic-sessions/', AcademicSessionListCreateView.as_view(), name='academic-session-list-create'),
    path('academic-sessions/<int:pk>/', AcademicSessionRetrieveUpdateDestroyView.as_view(), name='academic-session-retrieve-update-destroy'),

    # AcademicTerm URLs
    path('academic-terms/', AcademicTermListCreateView.as_view(), name='academic-term-list-create'),
    path('academic-terms/<int:pk>/', AcademicTermRetrieveUpdateDestroyView.as_view(), name='academic-term-retrieve-update-destroy'),

    # StudentClass URLs
    path('student-classes/', StudentClassListCreateView.as_view(), name='student-class-list-create'),
    path('student-classes/<int:pk>/', StudentClassRetrieveUpdateDestroyView.as_view(), name='student-class-retrieve-update-destroy'),

    # Subjects
    path('academic-subjects/',SubjectAPI.as_view()),
    path('academic-subjects/<int:pk>/',SubjectRetrieveUpdateDestroyView.as_view()),
    path('academic-class-subjects/',ClassSubjectRelationAPI.as_view()),
    path('academic-class-subjects/<int:pk>/',ClassSubjectRelationRetrieveUpdateDestroyView.as_view()),

    # Receipt URLs
    path('receipts/', ReceiptListCreateView.as_view(), name='receipt-list-create'),
    path('receipts/<int:pk>/', ReceiptRetrieveUpdateDestroyView.as_view(), name='receipt-retrieve-update-destroy'),

    path('schools/', SchoolListAPI.as_view(), name='school-list'),
    path('schools/create/', SchoolCreateAPI.as_view(), name='school-create'),
    path('schools/<int:pk>/', SchoolRetrieveAPI.as_view(), name='school-detail'),
    path('schools/<int:pk>/update/', SchoolUpdateAPI.as_view(), name='school-update'),
    path('schools/<int:pk>/delete/', SchoolDeleteAPI.as_view(), name='school-delete'),

     # Driver URLs
    path('drivers/', DriverListCreateView.as_view(), name='driver-list-create'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDestroyView.as_view(), name='driver-detail'),

    # Vehicle URLs
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicle-list-create'),
    path('vehicles/<int:pk>/', VehicleRetrieveUpdateDestroyView.as_view(), name='vehicle-detail'),

    # Route URLs
    path('routes/', RouteListCreateView.as_view(), name='route-list-create'),
    path('routes/<int:pk>/', RouteRetrieveUpdateDestroyView.as_view(), name='route-detail'),

    # Trip URLs
    path('trips/', TripListCreateView.as_view(), name='trip-list-create'),
    path('trips/<int:pk>/', TripRetrieveUpdateDestroyView.as_view(), name='trip-detail'),
]
