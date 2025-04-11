from apps.attendance.models import *
from apps.corecode.models import *
from apps.finance.models import *
from apps.result.models import *
from apps.staffs.models import *
from apps.user.models import *
from apps.students.models import *
from apps.transport.models import *
from apps.notifications.models import *
from .models import APKVersion, ErrorLog
from rest_framework import serializers
from django.contrib.auth.models import User,Permission
from django.shortcuts import get_object_or_404

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

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = StudentAttendance
        fields = '__all__'
    
    def get_student_name(self,obj):
        name = obj.student.get_fullname()
        return name
        

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
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

class UsersSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ('password',)
    
    def get_user_permissions(self, obj):
        return list(obj.get_all_permissions())

    def get_groups(self, obj):
        return [{"id": group.id, "name": group.name} for group in obj.groups.all()]
    
    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None


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

class InvoiceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.name", read_only=True)
    session = serializers.PrimaryKeyRelatedField(queryset=AcademicSession.objects.all())
    term = serializers.PrimaryKeyRelatedField(queryset=AcademicTerm.objects.all())
    month = serializers.ChoiceField(choices=Invoice.MONTH_CHOICES)
    class_for = serializers.PrimaryKeyRelatedField(queryset=StudentClass.objects.all())
    previous_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    tuition_fees = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    computer_fees = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    admission_fees = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    exam_fees = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    miscellaneous = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["total_payable"]

    def to_representation(self, instance):
        """Modify GET response to include student name, session name, and term name."""
        data = super().to_representation(instance)

        # Add additional fields for GET request
        data["session_name"] = instance.session.name
        data["term_name"] = instance.term.name
        data["student_name"] = instance.student.firstname + " "+ instance.student.surname
        data["registration_number"] = instance.student.registration_number
        data["class_name"] = instance.class_for.name
        data["total_payable"] = str(instance.balance())

        return data

    def validate(self, data):
        previous_balance = data.get("previous_balance", 0)
        class_for = data.get("class_for")

        # Get class fees
        tuition_fees = data.get("tuition_fees", class_for.tuition_fees)
        computer_fees = data.get("computer_fees", class_for.computer_fees)
        admission_fees = data.get("admission_fees", class_for.admission_fees)
        exam_fees = data.get("exam_fees", class_for.exam_fees)
        miscellaneous = data.get("miscellaneous", class_for.miscellaneous)

        # Compute total payable
        total_payable = (
            previous_balance +
            tuition_fees + computer_fees +
            admission_fees + exam_fees +
            miscellaneous
        )
        data["total_payable"] = total_payable
        data['previous_balance'] = total_payable
        return data

    def create(self, validated_data):
        class_for = validated_data.pop("class_for")
        tuition_fees = validated_data.pop("tuition_fees", class_for.tuition_fees)
        computer_fees = validated_data.pop("computer_fees", class_for.computer_fees)
        admission_fees = validated_data.pop("admission_fees", class_for.admission_fees)
        exam_fees = validated_data.pop("exam_fees", class_for.exam_fees)
        miscellaneous = validated_data.pop("miscellaneous", class_for.miscellaneous)

        invoice = Invoice.objects.create(**validated_data, class_for=class_for)

        fee_data = {
            "Tuition Fees": tuition_fees,
            "Computer Fees": computer_fees,
            "Admission Fees": admission_fees,
            "Exam Fees": exam_fees,
            "Miscellaneous": miscellaneous,
        }
        
        for description, amount in fee_data.items():
            InvoiceItem.objects.create(
                invoice=invoice,
                description=description,
                amount=amount,
                class_for=class_for
            )

        return invoice

class InvoiceDetailSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)
    receipts = ReceiptSerializer(many=True)
    registration_number = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()
    term = serializers.SerializerMethodField()
    student_class = serializers.SerializerMethodField()
    amount_payable = serializers.SerializerMethodField()
    total_amount_payable = serializers.SerializerMethodField()
    total_amount_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = '__all__'
    
    def get_balance(self,obj):
        return obj.balance()
    
    def get_amount_payable(self,obj):
        return obj.amount_payable()
    
    
    def get_total_amount_payable(self,obj):
        return obj.total_amount_payable()
    
    def get_total_amount_paid(self,obj):
        return obj.total_amount_paid()
    
    def get_registration_number(self,obj):
        return obj.student.registration_number

    def get_student_name(self,obj):
        return obj.student.get_fullname()

    def get_student_class(self,obj):
        return obj.class_for.name
    
    def get_term(self, obj):
        return obj.term.name
    
    def get_session(self,obj):
        return obj.session.name

class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = '__all__'
    
    

class SubjectClassSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    class Meta:
        model= ClassSubjectRelation
        fields = '__all__'
    
    def get_subject_name(self,obj):
        return obj.subject.name
    
    def get_class_name(self,obj):
        return obj.class_id.name

class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()
    term_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    class Meta:
        model = Result
        fields = '__all__'
    
    def get_student_name(self, obj):
        return obj.student.get_fullname()
    
    def get_session_name(self,obj):
        return obj.session.name
    
    def get_term_name(self,obj):
        return obj.term.name
    
    def get_class_name(self,obj):
        return obj.current_class.name
    
    def get_subject_name(self,obj):
        return obj.subject.name




class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class ShoutOutSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    class Meta:
        model = ShoutOut
        fields = '__all__'

class DeliveredNotificationSerializer(serializers.ModelSerializer):
    header = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = DeliveredNotification
        fields = '__all__'
    
    def get_message(self,obj):
        content_type = obj.content_type
        if content_type == 'Notification':
            object = get_object_or_404(Notification, id=obj.object_id)
            return object.message
        
        elif content_type == 'Announcement':
            object = get_object_or_404(Announcement, id=obj.object_id)
            return object.message
        
        elif content_type == 'ShoutOut':
            object = get_object_or_404(ShoutOut, id=obj.object_id)
            return object.message
    
    def get_header(self,obj):
        content_type = obj.content_type
        if content_type == 'Notification':
            object = get_object_or_404(Notification, id=obj.object_id)
            return object.title
        
        elif content_type == 'Announcement':
            object = get_object_or_404(Announcement, id=obj.object_id)
            return object.title
        
        elif content_type == 'ShoutOut':
            object = get_object_or_404(ShoutOut, id=obj.object_id)
            return object.title

