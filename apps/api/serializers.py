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


