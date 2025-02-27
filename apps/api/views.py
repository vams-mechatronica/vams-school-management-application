from django.shortcuts import render
from .models import *
from .serializers import *
from .pagination import LargeResultsSetPagination,StandardResultsSetPagination
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
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
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
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
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
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
        student_group, _ = Group.objects.get_or_create(name="Student")
        user.groups.add(student_group)

        # Generate unique registration number
        reg_number = f"VAMS/{timezone.now().year}/{timezone.now().strftime('%m%d%H%M%S')}"

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