from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *


# Create your views here.


@api_view(['GET'])
def hello(request):
    return Response({"hello":"Hello"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    employee = Employee.objects.get(user=user)
    return Response({'id':request.user.id,'username':request.user.username,'email':request.user.email,'firstname':request.user.first_name,'lastname':request.user.last_name,'domain':employee.domain})
