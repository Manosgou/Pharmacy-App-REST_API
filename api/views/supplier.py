from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import JSONParser
from api.models import Medicine,Employee,MedicineCategory,Order
from  api.serializers import MedicineSerializer,MedicineCategorySerializer,GetAllOrdersSerializer,OrderStatusSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medicine_category(request):     
    if request.method =='POST':
        data = JSONParser().parse(request)
        serializer = MedicineCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success':'Medicine category saved'},status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medicine_categories(request):
    categories = MedicineCategorySerializer(MedicineCategory.objects.all(),many=True)
    return Response(categories.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine_category(request,id):
    try:
        medicine_category = MedicineCategory.objects.get(id=id)
    except MedicineCategory.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='PUT':
        data = JSONParser().parse(request)
        serializer = MedicineCategorySerializer(medicine_category, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medicine_category(request,id):
    try:
        medicine_category = MedicineCategory.objects.get(id=id)
    except MedicineCategory.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='DELETE':
        medicine_category.delete()
        return HttpResponse(status=204)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medicine(request):
    employee = Employee.objects.get(user=request.user)
    if request.method =='POST' and employee.domain =='SP':
        data = JSONParser().parse(request)
        serializer = MedicineSerializer(data=data)
        if serializer.is_valid():
            employee = Employee.objects.get(user=request.user)
            serializer.validated_data['created_by']=employee
            serializer.save()
            return JsonResponse({'success':'Medicine saved'},status=201)
        return JsonResponse(serializer.errors, status=400)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medicines(request):
    employee = Employee.objects.get(user=request.user)
    medicines = MedicineSerializer(Medicine.objects.filter(created_by=employee),many=True)
    return Response(medicines.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine(request,id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='PUT':
        data = JSONParser().parse(request)
        serializer = MedicineSerializer(medicine, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medicine(request,id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='DELETE':
        medicine.delete()
        return HttpResponse(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = GetAllOrdersSerializer(Order.objects.all(),many=True)
    return Response(orders.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request,id):
    employee = Employee.objects.get(user=request.user)
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='PUT'and employee.domain =='SP':
        data = JSONParser().parse(request)
        serializer = OrderStatusSerializer(order,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)