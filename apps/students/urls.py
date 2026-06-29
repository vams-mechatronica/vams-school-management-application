from django.urls import path

from .views import (
    ClassCardSelectView,
    DownloadCSVView,
    StudentAdmitCardBulkView,
    StudentAdmitCardView,
    StudentBulkUploadView,
    StudentCreateView,
    StudentDeleteView,
    StudentDetailView,
    StudentIDCardBulkView,
    StudentIDCardView,
    StudentListView,
    StudentUpdateView,
    StudentDashboardView,
    StudentPromotionView,
    get_students_by_class
)

urlpatterns = [
    path("list", StudentListView.as_view(), name="student-list"),
    path("<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("dashboard/<int:pk>/", StudentDashboardView.as_view(), name="student-dashboard"),
    path("create/", StudentCreateView.as_view(), name="student-create"),
    path("<int:pk>/update/", StudentUpdateView.as_view(), name="student-update"),
    path("delete/<int:pk>/", StudentDeleteView.as_view(), name="student-delete"),
    path("upload/", StudentBulkUploadView.as_view(), name="student-upload"),
    path("download-csv/", DownloadCSVView.as_view(), name="download-csv"),
    path('promote-students/', StudentPromotionView.as_view(), name='promote-students'),
    path('ajax/get-students/<int:class_id>/', get_students_by_class, name='ajax_get_students'),

    path('id-card/<int:pk>/', StudentIDCardView.as_view(), name='student-id-card'),
    path('id-cards/select-class/', ClassCardSelectView.as_view(), {'card_type': 'id-card'}, name='id-card-select-class'),
    path('id-cards/class/<int:class_id>/', StudentIDCardBulkView.as_view(), name='student-id-card-bulk'),

    path('admit-card/<int:pk>/', StudentAdmitCardView.as_view(), name='student-admit-card'),
    path('admit-cards/select-class/', ClassCardSelectView.as_view(), {'card_type': 'admit-card'}, name='admit-card-select-class'),
    path('admit-cards/class/<int:class_id>/', StudentAdmitCardBulkView.as_view(), name='student-admit-card-bulk'),
]

