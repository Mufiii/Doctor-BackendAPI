from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)
    is_doctor = serializers.BooleanField(default=False,required=False)
    
    class Meta:
        model = MyUser
        fields = ('id','username','email','password','confirm_password','is_doctor')
        
    def validate(self,data):
      print(data)
      password = data.get('password')
      confirm_password = data.get('confirm_password')
      if password != confirm_password :
          raise serializers.ValidationError("password does not match")
      return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        return token
    
    

class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    hospital = serializers.CharField(required=False)
    department = serializers.CharField(required=False)
    
    class Meta:
        model = Doctor
        fields = ['id','hospital','department','user']
        read_only_fields = ('user',)
        
        
  
class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    
    class Meta :
        model = MyUser
        fields = ('id','first_name','last_name','username','email')
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        users = args[0]
        if users.is_doctor :
            self.fields['doctor'] = DoctorSerializer()
            
   
    def update(self,instance,validated_data):
        print(instance,'innn/////////')
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        print(instance.first_name,'first........')
        print(instance.last_name,'last........')
        
        if instance.is_doctor:
            doctor_data = validated_data.get('doctor')
            if doctor_data :
                doctor = Doctor.objects.filter(user=instance)
                if doctor.exists():
                    doctor = doctor.first()
                    doctor.hospital = doctor_data.get('hospital', doctor.hospital)
                    doctor.department = doctor_data.get('department', doctor.department)
                    if doctor.hospital is not None and doctor.department is not None:
                        doctor.is_verified=True
                    doctor.save()
                else:
                    raise ValidationError("No doctor record found for this user.")
                
        instance.save()
        return instance
                    


class UserViewAdminSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)   
    class Meta:
        model = MyUser
        fields = ('id','first_name', 'last_name','username', 'email','is_doctor','is_active','doctor')

    def update(self,instance,validated_data):
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance
