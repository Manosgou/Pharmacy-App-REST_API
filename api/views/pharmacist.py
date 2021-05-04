from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import *
from rest_framework.parsers import JSONParser
from api.models import Employee,Medicine,Order
from api.serializers import MedicineSerializer,CreateOrderSerializer,GetOrderSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medicines(request):
    employee = Employee.objects.get(user=request.user)
    medicines = MedicineSerializer(Medicine.objects.filter(created_by=employee),many=True)
    return Response(medicines.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_order(request):
    if request.method =='POST':
        data = JSONParser().parse(request)
        serializer = CreateOrderSerializer(data=data,many=True)
        if serializer.is_valid():
            for d in data:
                medicine_id = d['medicine']
                order_quantity=d['quantity']
                medicine = Medicine.objects.get(id=medicine_id)
                medicine.quantity = medicine.quantity - int(order_quantity)
                medicine.save()
            serializer.save()
            return JsonResponse({'success':'Order saved'},status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    try:
        employee =  Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return HttpResponse(status=404)
    orders = GetOrderSerializer(Order.objects.filter(employee=employee),many=True)
    return Response(orders.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_medicine_available(request,id):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return HttpResponse(status=404)
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    
    try:
        medicine = Medicine.objects.get(id=order.medicine.id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if not medicine.created_by == employee:
        return JsonResponse({'error':'Το προϊόν είναι ήδη διαθέσιμο'},status=400)
    if request.method =='POST' and employee.domain =='PH':
        data = JSONParser().parse(request)
        obj = medicine
        obj.pk=None
        obj.quantity=order.quantity
        obj.price = data['price']
        obj.created_by = employee
        obj.save()
        return JsonResponse({'success':'Medicine is avaialable'},status=201)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine_price(request,id):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return HttpResponse(status=404)
    try:
        medicine = Medicine.objects.get(created_by=employee)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='PUT'and employee.domain =='PH':
        data = JSONParser().parse(request)
        medicine.price =  data['price']
        medicine.save()
        return JsonResponse({'success':'Medicine price updated'},status=201)
    