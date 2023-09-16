from django.contrib import admin
from django.urls import path
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.UserRegister.as_view()),
    path('login/',TokenObtainPairView.as_view()),
    path('profile/',views.UserProfile.as_view(),name='userprofile'),
    
    path('userprofile/',views.UserProfileView.as_view()),
    path('userprofile/<int:pk>/',views.UserProfileView.as_view(),name='editprofile'),
    path('doctorview/',views.UserDoctorView.as_view(),name='viewdoctor'),
]
