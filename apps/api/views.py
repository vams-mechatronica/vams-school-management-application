from django.shortcuts import render,get_object_or_404
from .models import *
from math import ceil
from .serializers import *
from .pagination import LargeResultsSetPagination,StandardResultsSetPagination
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import filters
from collections import defaultdict
from django.core.paginator import Paginator
from django.utils.timezone import localtime
from datetime import datetime, date
from django.db.models import F, Case, When, Value, Sum, OuterRef, Subquery, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .permissions import *
from rest_framework.authentication import BasicAuthentication,TokenAuthentication, SessionAuthentication
from urllib.parse import urlencode
# Driver API
class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

# Vehicle API
class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# Route API
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class RouteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

# Trip API
class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class TripRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer




class APKVersionAPI(APIView):
    def get(self,request):
        os = request.GET.get('os')
        if os:
            try:
                latest_apk = APKVersion.objects.filter(os=os).latest('uploaded_at')
                serializer = APKVersionSerializer(latest_apk)
                # if serializer.is_valid():
                return Response(serializer.data,status=status.HTTP_200_OK)
                # else:
                #     return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except APKVersion.DoesNotExist:
                return Response({'message':'No matching record found.'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'Please select OS.'},status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class StudentAPI(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
    filterset_fields = ['current_class','date_of_admission','registration_number','firstname','gender','user']
    search_fields = ['surname','firstname','other_name','father_name','mother_name','gender','date_of_birth','date_of_admission','current_class__name','adharcard_number','parent_mobile_number','registration_number','user']
    ordering = ['user']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.first().name == 'Staff' or self.request.user.groups.first().name == 'admin':
            return queryset
        elif self.request.user.groups.first().name == 'Student':
            return queryset.filter(user=self.request.user)
        
    

class StudentDetailAPI(generics.RetrieveAPIView):
    """API to get student details based on the authenticated user."""
    serializer_class = StudentSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get_object(self):
        """
        Return the student object associated with the authenticated user.
        """
        return Student.objects.get(user=self.request.user)

class StudentCreateAPI(generics.CreateAPIView):
    serializer_class = StudentCreateSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get_registration_number(self):
        student = self.get_queryset().latest('updated_at')
        if student:
            last_id = student.id
        else:
            import random
            last_id = random.randint(0,99999)
        
        try:
            school_short_name = SchoolDetail.objects.latest('updated_at').short_name
        except SchoolDetail.DoesNotExist:
            school_short_name = "VAMS"
        timestamp = timezone.now().strftime('%d')
        reg_number = f"{school_short_name}/{timezone.now().year}/{timezone.now().month}/{timestamp}/{last_id + 1}"
        return reg_number

    def create(self, request, *args, **kwargs):
        admin_user = request.user  # Get admin user from token
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        # Generate username (lastname.firstname) in lowercase
        lastname = data.get("surname", "").strip().lower()
        firstname = data.get("firstname", "").strip().lower()
        username = f"{lastname}.{firstname}" if lastname and firstname else None

        # Validate required fields
        if not firstname or not username or "date_of_birth" not in data:
            return Response({"error": "Missing required fields: firstname, surname, date_of_birth"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse date_of_birth to generate password
        try:
            dob = timezone.datetime.strptime(data["date_of_birth"], "%Y-%m-%d")
            dob_part = dob.strftime("%d%m")
            today_part = timezone.now().strftime("%d%m%Y")
            password = f"{dob_part}{firstname}{lastname}{today_part}#"
        except ValueError:
            return Response({"error": "Invalid date_of_birth format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        user, created = User.objects.get_or_create(username=username, defaults={
            "first_name": data["firstname"],
            "last_name": data.get("surname", ""),
        })

        if created:
            user.set_password(password)
            user.save()

        # Ensure 'Student' group exists and assign user to it
        student_group, _ = Group.objects.get_or_create(name="Student")
        user.groups.add(student_group)

        reg_number = self.get_registration_number()
        
        # Add user and generated registration number to request data
        data["user"] = user.id
        data["registration_number"] = reg_number

        # Serialize and save student record
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(
                {
                    "message": "Student created successfully",
                    "student_id": student.id,
                    "registration_number": student.registration_number,
                    "username": user.username,
                    "password": password if created else "User already exists",
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentUpdateAPI(generics.UpdateAPIView):
    """API to update an existing Student."""
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

class StudentDeleteAPI(generics.DestroyAPIView):
    """API to delete a Student, only if the user has delete permission."""
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminUser, CanDeleteStudent)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

class StudentBulkUploadAPI(generics.CreateAPIView):
    queryset = StudentBulkUpload.objects.all()
    serializer_class = StudentBulkUploadSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)

class StudentAttendanceAPI(generics.ListCreateAPIView):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('date', 'status', 'remarks', 'created_at', 'modified_at', 'student')
    search_fields = ('date', 'status', 'remarks', 'created_at', 'modified_at', 'student')

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get class_id from request parameters
        class_id = self.request.query_params.get('class')

        if class_id:
            queryset = queryset.filter(student__current_class_id=class_id)

        return queryset

    


class StaffBulkUploadAPI(generics.CreateAPIView):
    queryset = StaffBulkUpload.objects.all()
    serializer_class = StaffBulkCreateSerializer
    permission_classes = (IsAdminOrStaff, CanCreateStaff)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class StaffListAPI(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
    search_fields = ['surname','firstname','other_name','gender','date_of_birth','date_of_joining','adhar_card_number','mobile_number','user__id']
    ordering = ['id']

class StaffCreateAPI(generics.CreateAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    permission_classes = (IsAdminUser,CanCreateStaff)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def create(self, request, *args, **kwargs):
        admin_user = request.user  # Get admin user from token
        if not admin_user or not admin_user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        # Generate username (lastname.firstname) in lowercase
        lastname = data.get("surname", "").strip().lower()
        firstname = data.get("firstname", "").strip().lower()
        username = f"{lastname}.{firstname}" if lastname and firstname else None

        # Validate required fields
        if not firstname or not username or "date_of_birth" not in data:
            return Response({"error": "Missing required fields: firstname, surname, date_of_birth"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse date_of_birth to generate password
        try:
            dob = timezone.datetime.strptime(data["date_of_birth"], "%Y-%m-%d")
            dob_part = dob.strftime("%d%m")  # Extract ddmm from DOB
            today_part = timezone.now().strftime("%d%m%Y")  # Today's date
            password = f"{dob_part}{firstname}{lastname}{today_part}#"  # Password format
        except ValueError:
            return Response({"error": "Invalid date_of_birth format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        user, created = User.objects.get_or_create(username=username, defaults={
            "first_name": data["firstname"],
            "last_name": data.get("surname", ""),
        })

        if created:
            user.set_password(password)
            user.save()

        # Ensure 'Student' group exists and assign user to it
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        user.groups.add(staff_group)

        # Generate unique registration number
        emp_code = f"VAMS/{timezone.now().year}/{timezone.now().strftime('%m%d%H%M%S')}/{user.pk}"

        # Add user and generated registration number to request data
        data["user"] = user.id
        data["emp_code"] = emp_code

        # Serialize and save student record
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response(
                {
                    "message": "Student created successfully",
                    "student_id": staff.id,
                    "registration_number": staff.emp_code,
                    "username": user.username,
                    "password": password if created else "User already exists",
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = (IsAuthenticated, IsAdminOrStaff)

# AcademicSession Views
class AcademicSessionListCreateView(generics.ListAPIView):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class AcademicSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


# AcademicTerm Views
class AcademicTermListCreateView(generics.ListAPIView):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class AcademicTermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


# StudentClass Views
class StudentClassListCreateView(generics.ListAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)

class StudentClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


# Receipt Views
class ReceiptListCreateView(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class ReceiptRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)



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
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class SchoolRetrieveAPI(generics.RetrieveAPIView):
    """API to retrieve details of a single school"""
    serializer_class = SchoolDetailSerializer
    queryset = SchoolDetail.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = (BasicAuthentication,TokenAuthentication)


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


class DashboardDataAPIView(APIView):

    def get(self, request):
        today = now().date()
        # Get the current date and time (timezone-aware)
        nows = timezone.now()

        # Get the first day of the current month
        first_day_of_month = nows.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the last day of the current month
        next_month = (first_day_of_month + timezone.timedelta(days=31)).replace(day=1)
        last_day_of_month = next_month - timezone.timedelta(days=1)

        total_students = Student.objects.count()
        present_students = StudentAttendance.objects.filter(date=today, status=1).count()
        absent_students = total_students - present_students
        total_staff = Staff.objects.count()
        present_staff = StaffAttendance.objects.filter(date=today, status=1).count()
        absent_staff = total_staff-present_staff
        # Subquery to get the latest invoice for each student
        latest_invoice = Invoice.objects.filter(student=OuterRef('student')).order_by('-created_at')

        # Get the last created invoice for each student
        invoices = Invoice.objects.annotate(
            latest_created_at=Subquery(latest_invoice.values('created_at')[:1])
        ).filter(created_at=F('latest_created_at'))
        fees_balance = sum(invoice.balance() for invoice in invoices if invoice.balance() > 0)
        fees_received = Receipt.objects.filter(
            date_paid__gte=first_day_of_month,
            date_paid__lte=last_day_of_month
        ).aggregate(total_amount_paid=Sum('amount_paid'))['total_amount_paid']

        attendance_graph = {
            'labels': [],  # e.g., ['2023-01-01', '2023-01-02', ...]
            'present': [],  # e.g., [10, 20, ...]
            'absent': []    # e.g., [5, 3, ...]
        }

        # Assuming you have a method to get attendance data for the past week
        past_week_dates = [today - timedelta(days=i) for i in range(7)]
        for date in past_week_dates:
            present_students_date =StudentAttendance.objects.filter(date=date, status=1).count()
            absent_students_date = total_students - StudentAttendance.objects.filter(date=date, status=1).count()
            attendance_graph['labels'].append(date.strftime('%Y-%m-%d'))
            attendance_graph['present'].append(present_students_date)
            attendance_graph['absent'].append(absent_students_date)

        data = {
            'total_students': total_students,
            'present_students': present_students,
            'absent_students': absent_students,
            'total_staff': total_staff,
            'present_staff': present_staff,
            'absent_staff': absent_staff,
            'fees_balance': ceil(fees_balance) if fees_balance else 0,
            'fees_received': ceil(fees_received) if fees_received else 0,
            'attendance_graph': attendance_graph
        }

        return Response(data, status=status.HTTP_200_OK)

class StaffAttendenceAPI(generics.ListAPIView):
    queryset = StaffAttendance.objects.all()
    serializer_class = StaffAttendanceSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (TokenAuthentication,BasicAuthentication,SessionAuthentication)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
    filterset_fields = ['date','staff__id','staff__surname','staff__firstname','staff__emp_code']
    search_fields = ['date','staff__id','staff__surname','staff__firstname','staff__emp_code']
    ordering = ['date']

class StaffAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    
    def post(self, request):
        user = request.user
        today = now().date()
        current_time = localtime().time()
        getStaff = Staff.objects.get(user=user)
        
        try:
            attendance = StaffAttendance.objects.get(staff=getStaff, date=today)
            if not attendance.time_in:
                attendance.status = 1
                attendance.time_in = current_time
            else:
                attendance.time_out = current_time
            attendance.save()
            return Response({"message": "Attendance recorded", "data": StaffAttendanceSerializer(attendance).data})

        except StaffAttendance.DoesNotExist:
            attendance = StaffAttendance.objects.create(staff=getStaff, date=today, time_in=current_time,status=1)
            return Response({"message": "Time in recorded", "data": StaffAttendanceSerializer(attendance).data})

class UserProfileU(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserProfile(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = self.request.user

        if user.is_superuser:
            serializer = UserProfileSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        elif not user.is_superuser and user.is_staff:
            data = Staff.objects.get(user=user)
            serializer = StaffProfileSerializer(data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        else:
            data = Student.objects.get(user=user)
            serializer = StudentProfileSerializer(data)
            return Response(serializer.data,status=status.HTTP_200_OK)

class ErrorLogAPI(generics.ListCreateAPIView):
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorSerializer
    permission_classes = (AllowAny,)

from rest_framework import viewsets, status
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        group_name = user.groups.first().name if user.groups.exists() else None

        if group_name in ['admin', 'Staff']:
            return Invoice.objects.filter(status=True).order_by('-updated_at')
        elif group_name == 'Student':
            return Invoice.objects.filter(status=True, student__user=user).order_by('-updated_at')
        return Invoice.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj

    def retrieve(self, request, *args, **kwargs):
        """Fetch invoice (with class fees, prev balance if needed)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create invoice and compute total payable"""
        user = request.user
        group_name = user.groups.first().name if user.groups.exists() else None

        if group_name not in ['admin', 'Staff']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Update invoice with partial data (e.g. fees), keep class_for untouched"""
        user = request.user
        group_name = user.groups.first().name if user.groups.exists() else None

        if group_name not in ['admin', 'Staff']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailAPI(APIView):
    permission_classes = (IsAdminOrStaff | IsInvoiceOwner,)
    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    def get(self, request):
        invoice_id = request.GET.get('invoice_id', None)
        
        if not invoice_id:
            return Response({"error": "Invoice ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer = InvoiceDetailSerializer(invoice)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SubjectAPI(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer



class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)

class ClassSubjectRelationAPI(generics.ListCreateAPIView):
    queryset = ClassSubjectRelation.objects.all()
    serializer_class = SubjectClassSerializer



class ClassSubjectRelationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassSubjectRelation.objects.all()
    serializer_class = SubjectClassSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)

class UsersAPI(generics.ListAPIView):
    queryset = User.objects.all()
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAdminOrStaff,)
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['is_active','is_superuser']
    search_fields = ['username','first_name','last_name','email']

class StudentResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get_grade(self, obt_score, mm_score):
        perc = (float(obt_score) / float(mm_score)) * 100 if mm_score else 0
        if perc == 100:
            grade = 'A+'
        elif 90 <= perc < 100:
            grade = 'A'
        elif 80 <= perc < 90:
            grade = 'B+'
        elif 70 <= perc < 80:
            grade = 'B'
        elif 60 <= perc < 70:
            grade = 'C+'
        elif 50 <= perc < 60:
            grade = 'C'
        elif 40 <= perc < 50:
            grade = 'D+'
        elif 33 <= perc < 40:
            grade = 'D'
        else:
            grade = 'F'
        return grade
    
    def get_queryset(self, student_id):
        user = self.request.user
        if user.groups.first().name == 'Student':
            return [get_object_or_404(Student, user=user)]
        else:
            return [get_object_or_404(Student, id=student_id)] if student_id else Student.objects.all()
    

    def get(self, request):
        student_id = request.GET.get('student_id')
        students = self.get_queryset(student_id=student_id)

        session_name = request.query_params.get('session')
        term_name = request.query_params.get('term')
        class_name = request.query_params.get('class')
        subject_search = request.query_params.get('search')

        all_results = []

        for student in students:
            results = Result.objects.filter(student=student)

            if session_name:
                results = results.filter(session__name__icontains=session_name)
            if term_name:
                term_id = get_object_or_404(AcademicTerm, name=term_name)
                results = results.filter(term=term_id)
            if class_name:
                results = results.filter(current_class__name__icontains=class_name)
            if subject_search:
                results = results.filter(subject__name__icontains=subject_search)

            data = defaultdict(lambda: defaultdict(list))
            total_obt_score = 0
            total_max_score = 0

            for result in results:
                session = result.session.name
                term = result.term.name
                subject_max = result.subject.test_max_marks + result.subject.exam_max_marks
                subject_obt = result.test_score + result.exam_score

                total_max_score += subject_max
                total_obt_score += subject_obt

                subject_info = {
                    "subject_id": result.subject.id,
                    "subject": result.subject.name,
                    "test_score": result.test_score,
                    "exam_score": result.exam_score,
                    "total_score": result.total_score(),
                    "grade": result.calc_grade(),
                    "max_score": subject_max
                }
                data[session][term].append(subject_info)

            academic_results = []
            for session, terms in data.items():
                term_data = []
                for term, subjects in terms.items():
                    term_total = sum(sub["total_score"] for sub in subjects)
                    term_max = sum(sub["max_score"] for sub in subjects)
                    term_grade = self.get_grade(term_total, term_max)
                    term_remarks = "Pass" if term_grade != 'F' else "Fail"

                    term_data.append({
                        "term": term,
                        "subjects": subjects,
                        "overall": {
                            "total_score": term_total,
                            "max_score": term_max,
                            "grade": term_grade,
                            "remarks": term_remarks
                        }
                    })
                academic_results.append({
                    "academic_year": session,
                    "terms": term_data
                })

            # Overall for student
            overall_grade = self.get_grade(total_obt_score, total_max_score)
            overall_remarks = "Pass" if overall_grade != 'F' else "Fail"

            if academic_results:
                all_results.append({
                    "student_id": student.id,
                    "student_name": student.get_fullname(),
                    "roll_number":student.roll_number,
                    "student_class": student.current_class.name,
                    "academic_results": academic_results,
                    "overall": {
                        "total_score": total_obt_score,
                        "max_score": total_max_score,
                        "grade": overall_grade,
                        "remarks": overall_remarks
                    }
                })

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        paginator = Paginator(all_results, page_size)
        current_page = paginator.get_page(page)

        def build_page_url(page_number):
            if page_number > paginator.num_pages or page_number < 1:
                return None
            query_params = request.query_params.copy()
            query_params['page'] = page_number
            return request.build_absolute_uri(f"?{urlencode(query_params)}")

        return Response({
            "count": paginator.count,
            "next": build_page_url(current_page.next_page_number()) if current_page.has_next() else None,
            "previous": build_page_url(current_page.previous_page_number()) if current_page.has_previous() else None,
            "results": list(current_page),
        })


class NotificationListAPI(generics.ListAPIView):
    serializer_class = DeliveredNotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['mark_as_read']

    def get_queryset(self):
        return DeliveredNotification.objects.filter(user=self.request.user).order_by('-delivered_at')

class NotificationMarkAsReadAPI(APIView):
    def post(self,request):
        data = request.data
        notification_id = data.get('notification_id')
        if notification_id:
           noti = DeliveredNotification.objects.get(id=notification_id)
           noti.mark_as_read = True
           noti.save()
           return Response({'message':'Notification marked as read'},status=status.HTTP_200_OK)
        return Response({'message':'Notification Id is mandatory'},status=status.HTTP_400_BAD_REQUEST)


class PromoteStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_class_id = request.data.get("new_class_id")
        student_ids = request.data.get("student_ids", [])

        if not new_class_id or not student_ids:
            return Response({"error": "Missing required fields"}, status=400)

        students = Student.objects.filter(id__in=student_ids)
        for student in students:
            student.current_class = new_class_id
            student.save()

            unpaid_invoices = Invoice.objects.filter(student=student, status=True)
            for inv in unpaid_invoices:
                Invoice.objects.create(
                    student=student,
                    month=inv.month,
                    previous_balance = inv.balance(),
                    total_payable = inv.balance(),
                    due_date=date.today() + timedelta(days=15),
                    status=True
                )

        return Response({"message": "Students promoted successfully."})
