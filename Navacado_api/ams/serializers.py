from .models import Department, Faculty, Class, Batch, Student, Course,Enrollment, Lecture, Lab, Timetable, TimeTableSlot, LecAttendance, LabAttendance,UserProfile
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['profileid']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['id']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'
        read_only_fields = ['id']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        read_only_fields = ['id']


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
        read_only_fields = ['id']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['uid']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ['cid']
        fields = '__all__'
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        read_only_fields = ['id']
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ['id']


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'
        read_only_fields = ['id']


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'
        read_only_fields = ['id']


class TimeTableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTableSlot
        fields = '__all__'
        read_only_fields = ['id']


class LecAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecAttendance
        fields = '__all__'
        read_only_fields = ['id']


class LabAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabAttendance
        fields = '__all__'
        read_only_fields = ['id']

class LectureCountSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    lec_count = serializers.IntegerField()
    class Meta:
        read_only_fields = ['course','lec_count']

class LabCountSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    lab_count = serializers.IntegerField()
    class Meta:
        read_only_fields = ['course','lab_count']

class LabAttendacnceStatSerializer(serializers.Serializer):
    Course = serializers.IntegerField()
    TotalLabs = serializers.IntegerField()
    LabsAttended = serializers.IntegerField()
    PercentAttendance = serializers.FloatField()   

class LecAttendacnceStatSerializer(serializers.Serializer):
    Course = serializers.IntegerField()
    TotalLecs = serializers.IntegerField()
    LecsAttended = serializers.IntegerField()
    PercentAttendance = serializers.FloatField()   
   
class UserSerializer(ModelSerializer):
   class Meta:
       model = User
       fields ='__all__'
       extra_kwargs = {'password': {'write_only': True}}
   def create(self, validated_data):
       user = User.objects.create_user(**validated_data)  # ** operator --> validated_data = {
#     'username': 'john_doe',
#     'email': 'john@example.com',  
#     'password': 'securepassword123'  to  user = User.objects.create_user(username='john_doe', email='john@example.com', password='securepassword123')
       return user
# }
