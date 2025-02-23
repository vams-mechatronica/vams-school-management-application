from apps.attendance.models import *
from apps.corecode.models import *
from apps.finance.models import *
from apps.result.models import *
from apps.staffs.models import *
from apps.user.models import *
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

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

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'

class AcademicTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTerm
        fields = '__all__'

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class SchoolDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDetail
        fields = '__all__'



