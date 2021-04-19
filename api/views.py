from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import *
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from api.models import *


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
    user = UserSerializer(request.user)
    return Response({'user':user.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request,id):
    if request.method=='PUT':
        try:
            user = User.objects.get(id=id)
        except user.DoesNotExist:
            return HttpResponse(status=404) 
        

        data = JSONParser().parse(request)
        serializer = UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

