from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.fields import DateField
from rest_framework.serializers import Serializer


User = get_user_model()

# --- Authentication Serializers ---

class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
    

class DateFilterSerializer(Serializer):
    start_date = DateField(required=True)
    end_date = DateField(required=True)

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
    

class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"   


class GetTeachersByIdsSerializer(serializers.Serializer):
    teacher_ids = serializers.ListField(child=serializers.IntegerField())
    

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","password","full_name","phone")
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

# --- Attendance Serializers ---
class AttendanceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLevel
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

# --- Courses Serializer ---
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

# --- Groups Serializer ---
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

# --- Homework Serializers ---
class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'

class GroupHomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupHomeWork
        fields = '__all__'

class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = '__all__'

# --- Table Types and Tables Serializers ---
class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['group', 'course', 'descriptions']

# Ota-ona serializeri
class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True,read_only=True)

    class Meta:
        model = Parent
        fields = ('id','name','surname','address','phone','description','students')

# Student va ota-onani yaratish uchun serializer
class UserAndStudentSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        student_data = validated_data.pop('student')
       
        # User yaratish
        user = User.objects.create_user(**user_data, is_student=True)

        # Student yaratish
        student = Student.objects.create(user=user, **student_data)

        return {'user': user, 'student': student}



# --- Worker Serializer ---
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

# --- Comment Serializer ---
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# --- Password Management Serializers ---
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({"old_password": "Eski parol noto‘g‘ri"})
        return data


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            raise serializers.ValidationError({"error": "Bunday foydalanuvchi mavjud emas"})
        user.otp_code = "123456"  # OTP
        user.save()
        return data

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()

class SetNewPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(phone=data['phone'], otp_code=data['otp']).first()
        if not user:
            raise serializers.ValidationError({"error": "Foydalanuvchi topilmadi yoki OTP noto‘g‘ri"})

        user.password = make_password(data['new_password'])
        user.otp_code = None  #  OTP kodni o‘chiramiz
        user.save()
        return data
    
class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    pass  

# Teacher serializer
class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Teacher
        fields = ('id','user', 'cource', 'description')

# Teacher va userni yaratish uchun serializer
class UserAndTeacherSerializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        teacher_data = validated_data.pop('teacher')

        # User yaratish
        user = User.objects.create_user(**user_data, is_teacher=True)

        # Teacher yaratish
        teacher = Teacher.objects.create(user=user, **teacher_data)

        return {'user': user, 'teacher': teacher}
    

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "full_name", "is_active", "is_student", "is_teacher"]


class SuperUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "password", "full_name"]

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user


class StudentStatisticSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class TeacherStatisticSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class AttendanceStatisticSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class CourseStatisticSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class GroupStatisticSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class MockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockData
        fields = "__all__"
        

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
        
