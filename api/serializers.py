from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=['domain']


class UserSerializer(serializers.ModelSerializer):
    employee =EmployeeSerializer(required=False)
    class Meta:
        model=User
        fields=['id','username','email','last_name','first_name','employee']