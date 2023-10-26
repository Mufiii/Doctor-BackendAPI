from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.authentication import authenticate
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from .custompermission import UserPermision
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView,TokenBlacklistView
# Create your views here.


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        
        if serializer.is_valid():
          user = MyUser.objects.create_user(
            username = serializer.validated_data['username'],
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password'],
            is_doctor = serializer.validated_data['is_doctor']
          )
          print(user) 
          return Response({'msg':'User Registered Successfully'}, status=status.HTTP_201_CREATED)
        
        return Response( {'msg':serializer.errors } , status=status.HTTP_400_BAD_REQUEST)
      
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
      
# @authentication_classes([JWTAuthentication]) 
class UserProfile(APIView):
  
    def get(self, request):  
          
          user = MyUser.objects.get(pk=request.user.id)
          serializer = UserProfileSerializer(user)
          return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request):
      print(request.data)
      serializer = UserProfileSerializer(request.user , data = request.data, partial=True )
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
      return Response({'msg':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user = MyUser.objects.get(id=request.user.id)
        print("dde",user)
        user.delete()
        return Response({'msg':'User Deleted Successfully'} , status=status.HTTP_200_OK)      



@permission_classes([IsAdminUser])
class   UserProfileView(APIView):
    def get(self,request,pk=None):
      if pk is None:
          user = MyUser.objects.exclude(is_admin=True)
          serializer = UserViewAdminSerializer(user, many=True)
          return Response(serializer.data)
      user = MyUser.objects.get(pk=pk)
      serializer = UserViewAdminSerializer(user)
      return Response(serializer.data)
    
    
    def patch(self,request,pk=None) :
        if pk is not None:
          user = MyUser.objects.get(pk=pk)
          serializers = UserViewAdminSerializer(user, data = request.data , partial=True)
          if serializers.is_valid():
            serializers.save()
            if serializers.validated_data['is_active']:
                return Response({"msg":"User Unblocked !!!!"},status=status.HTTP_200_OK)
            return Response({"msg":"User Blocked !!!"},status=status.HTTP_200_OK)
          return Response(serializers.errors)


permission_classes([UserPermision])
class UserDoctorView(APIView):
    def get(self,request):
        q = request.GET.get('q')
        Q_Base = Q(doctor__is_verified=True) & Q(is_active=True)
        user = MyUser.objects.filter(Q_Base)
        search_query = Q()
        if q:
            search_query = Q(username__icontains=q)|Q(doctor__department__icontains=q)|Q(doctor__hospital__icontains=q)
            Q_Base &= search_query 
        user = MyUser.objects.filter(Q_Base)
        serializer = UserViewAdminSerializer(user,many=True)
          
        return Response(serializer.data,status=status.HTTP_200_OK)
    