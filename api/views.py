from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


# Create your views here.


@api_view(['GET'])
def hello(request):
    return Response({"hello":"Hello"})
