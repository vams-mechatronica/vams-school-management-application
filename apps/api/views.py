from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsStaff, CanDeleteStudent, IsAdminOrStaff, IsInvoiceOwner, IsStudent, CanDeleteSchool
from rest_framework.authentication import BasicAuthentication,TokenAuthentication

# Create your views here.
class StudentAPI(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = '__all__'
    ordering = ['user_id']

class StudentDetailAPI(generics.RetrieveAPIView):
    """API to get student details based on the authenticated user."""
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get_object(self):
        """
        Return the student object associated with the authenticated user.
        """
        return Student.objects.get(user=self.request.user)

class StudentCreateAPI(generics.CreateAPIView):
    serializer_class= StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminUser,IsStaff)
    authentication_classes = (BasicAuthentication,TokenAuthentication)

class StudentUpdateAPI(generics.UpdateAPIView):
    """API to update an existing Student."""
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

class StudentDeleteAPI(generics.DestroyAPIView):
    """API to delete a Student, only if the user has delete permission."""
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminUser, CanDeleteStudent)
    authentication_classes = (BasicAuthentication, TokenAuthentication)


class StaffListCreateView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)


class StaffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff or self.request.user.is_superuser:
            serializer.save()

class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated, IsAdminOrStaff | IsInvoiceOwner)

# AcademicSession Views
class AcademicSessionListCreateView(generics.ListCreateAPIView):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = (IsAdminOrStaff,)

class AcademicSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = (IsAdminOrStaff,)

# AcademicTerm Views
class AcademicTermListCreateView(generics.ListCreateAPIView):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = (IsAdminOrStaff,)

class AcademicTermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = (IsAdminOrStaff,)

# StudentClass Views
class StudentClassListCreateView(generics.ListCreateAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    permission_classes = (IsAdminOrStaff,)

class StudentClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    permission_classes = (IsAdminOrStaff,)

# Receipt Views
class ReceiptListCreateView(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (IsAdminOrStaff,)

class ReceiptRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (IsAdminOrStaff,)


class SchoolCreateAPI(generics.CreateAPIView):
    """API to create a new school"""
    serializer_class = SchoolDetailSerializer
    queryset = SchoolDetail.objects.all()
    permission_classes = [IsAdminUser]  # Only admin can create
    authentication_classes = [TokenAuthentication, BasicAuthentication]

class SchoolListAPI(generics.ListAPIView):
    """API to list all schools"""
    serializer_class = SchoolDetailSerializer
    queryset = SchoolDetail.objects.all()
    permission_classes = [AllowAny]  # Anyone can view list

class SchoolRetrieveAPI(generics.RetrieveAPIView):
    """API to retrieve details of a single school"""
    serializer_class = SchoolDetailSerializer
    queryset = SchoolDetail.objects.all()
    permission_classes = [AllowAny]

class SchoolUpdateAPI(generics.UpdateAPIView):
    """API to update school details"""
    serializer_class = SchoolDetailSerializer
    queryset = SchoolDetail.objects.all()
    permission_classes = [IsAdminUser]  # Only admin can update
    authentication_classes = [TokenAuthentication, BasicAuthentication]

class SchoolDeleteAPI(generics.DestroyAPIView):
    """API to delete a school (Only users with delete permission)"""
    serializer_class = SchoolDetailSerializer
    queryset = SchoolDetail.objects.all()
    permission_classes = [IsAdminUser, CanDeleteSchool]  # Custom delete permission
    authentication_classes = [TokenAuthentication, BasicAuthentication]