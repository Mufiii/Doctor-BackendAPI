from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(MyUser)
class adminuser(admin.ModelAdmin):
    list_display = ['id','username','email']
    

@admin.register(Doctor)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','user','hospital','department']