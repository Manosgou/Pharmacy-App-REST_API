from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import LocationSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.models import Location,Order,Medicine,Employee


# Create your views here.


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print("Hello")
        return Response({
            'token': token.key,
            'domain': user.employee.domain,
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    data={}
    user = UserSerializer(request.user)
    data['user'] = user.data
    if request.user.employee.domain == 'PH':
        obj,created = Location.objects.get_or_create(employee=request.user.employee)
        location = LocationSerializer(obj)
        data['location'] = location.data
    elif request.user.employee.domain == 'SP':
        last_order = Order.objects.last()
        last_medicine = Medicine.objects.last()
        data['last_order'] = {"full_name":last_order.employee.user.first_name+" "+last_order.employee.user.last_name,"medicine":last_order.medicine.name,"quantity":last_order.quantity,"total_price":last_order.total_price}
        data['last_medicine'] ={"name":last_medicine.name,"category":last_medicine.category.name,"quantity":last_medicine.quantity,"price":last_medicine.price}
    return JsonResponse(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def location_update(request,id):
    if request.method =='PUT':
        try:
            employee = Employee.objects.get(id=id)
            location,created = Location.objects.get_or_create(employee=employee)
        except Location.DoesNotExist:
            return HttpResponse(status=404)
        
        data = JSONParser().parse(request)
        serializer = LocationSerializer(location,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success':'Location updated'}, status=201)
        return JsonResponse(serializer.errors, status=400)




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
            return JsonResponse({'success':'User updated'}, status=201)
        return JsonResponse(serializer.errors, status=400)