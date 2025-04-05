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
from django.db.models import F, Case, When, Value, Sum, OuterRef, Subquery, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsStaff, CanDeleteStudent, IsAdminOrStaff, IsInvoiceOwner, IsStudent, CanDeleteSchool
from rest_framework.authentication import BasicAuthentication,TokenAuthentication, SessionAuthentication

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
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
    filterset_fields = ['current_class','date_of_admission','registration_number','firstname','gender']
    search_fields = ['surname','firstname','other_name','father_name','mother_name','gender','date_of_birth','date_of_admission','current_class__name','adharcard_number','parent_mobile_number','registration_number','user__id']
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
    serializer_class = StudentCreateSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAdminUser,)
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
    permission_classes = (IsAdminUser,)
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
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class StaffListAPI(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
    search_fields = ['surname','firstname','other_name','gender','date_of_birth','date_of_joining','adhar_card_number','mobile_number','user__id']
    ordering = ['id']

class StaffCreateAPI(generics.CreateAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    permission_classes = (IsAdminUser,)
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
    permission_classes = (IsAuthenticated, IsAdminOrStaff | IsInvoiceOwner)

# AcademicSession Views
class AcademicSessionListCreateView(generics.ListCreateAPIView):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class AcademicSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


# AcademicTerm Views
class AcademicTermListCreateView(generics.ListCreateAPIView):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


class AcademicTermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = (IsAdminOrStaff,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)


# StudentClass Views
class StudentClassListCreateView(generics.ListCreateAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    permission_classes = (IsAdminOrStaff,)
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
        absent_students = StudentAttendance.objects.filter(date=today, status=0).count()
        total_staff = Staff.objects.count()
        present_staff = StaffAttendance.objects.filter(date=today, status=1).count()
        absent_staff = StaffAttendance.objects.filter(date=today, status=0).count()
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
            attendance_graph['labels'].append(date.strftime('%Y-%m-%d'))
            attendance_graph['present'].append(StudentAttendance.objects.filter(date=date, status=1).count())
            attendance_graph['absent'].append(StudentAttendance.objects.filter(date=date, status=0).count())

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
        current_time = now().time()
        getStaff = Staff.objects.get(user=user)
        
        try:
            attendance = StaffAttendance.objects.get(staff=getStaff, date=today)
            if attendance:
                attendance.time_out = current_time
                attendance.save()
                return Response({"message": "Time out recorded", "data": StaffAttendanceSerializer(attendance).data})

        except StaffAttendance.DoesNotExist:
            attendance = StaffAttendance.objects.create(staff=getStaff, date=today, time_in=current_time)
            return Response({"message": "Time in recorded", "data": StaffAttendanceSerializer(attendance).data})

class UserProfile(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
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
    queryset = Invoice.objects.filter(status=True).order_by('-updated_at')
    serializer_class = InvoiceSerializer

    def retrieve(self, request, *args, **kwargs):
        """ Fetch student invoice with previous balance and class fees """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """ Create invoice and compute total_payable """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """ Update invoice, allowing fee edits but keeping class_for unchanged """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceDetailAPI(APIView):
    def get(self, request):
        invoice_id = request.GET.get('invoice_id', None)
        
        if not invoice_id:
            return Response({"error": "Invoice ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer = InvoiceDetailSerializer(invoice)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    