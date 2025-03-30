from apps.attendance.models import *
from apps.corecode.models import *
from apps.finance.models import *
from apps.result.models import *
from apps.staffs.models import *
from apps.user.models import *
from apps.students.models import *
from apps.transport.models import *
from .models import APKVersion, ErrorLog
from rest_framework import serializers
from django.contrib.auth.models import User,Permission

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'  # Includes all fields

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    route_name = serializers.ReadOnlyField(source='route.name')
    vehicle_number = serializers.ReadOnlyField(source='vehicle.vehicle_number')
    driver_name = serializers.ReadOnlyField(source='driver.name')

    class Meta:
        model = Trip
        fields = '__all__'


class APKVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = APKVersion
        fields = ['version', 'file','os','uploaded_at']

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    current_class = serializers.CharField(source='current_class.name', read_only=True)
    class Meta:
        model = Student
        fields = '__all__'

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentBulkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StudentBulkUpload
        exclude = ('date_uploaded',)

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
    
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class StaffBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffBulkUpload
        exclude = ('date_uploaded',)

class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = '__all__'

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'

class AcademicTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTerm
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    session = AcademicSessionSerializer()
    term = AcademicTermSerializer()
    class_for = StudentClassSerializer()

    class Meta:
        model = Invoice
        fields = '__all__'

class SchoolDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDetail
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Permission
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password',)

    def get_user_permissions(self, obj):
        return list(obj.get_all_permissions())

    def get_groups(self, obj):
        return [{"id": group.id, "name": group.name} for group in obj.groups.all()]


class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Staff
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Student
        fields = '__all__'

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'