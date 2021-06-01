from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import *
from rest_framework.parsers import JSONParser
from api.models import Medicine,UserProfile,Order
from api.serializers import CreateOrderSerializer,MedicineSerializer,GetOrderSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medicines(request):
    try:
        user_profile = UserProfile.objects.get(domain='PH')
    except UserProfile.DoesNotExist:
        return HttpResponse(status=404)
    try:
        medicines = MedicineSerializer(Medicine.objects.filter(created_by=user_profile),many=True)
    except Medicine.DoesNotExist:
        return HttpResponse(status=404)
    return Response(medicines.data)



@api_view(['GET','POST'])
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
    user_profile = UserProfile.objects.get(domain='PH')
    try:
        medicines = MedicineSerializer(Medicine.objects.filter(created_by=user_profile),many=True)
    except Medicine.DoesNotExist:
        return HttpResponse(status=404)
    return Response(medicines.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    current_user = request.user
    try:
        user_profile = UserProfile.objects.get(user=current_user)
    except UserProfile.DoesNotExist:
        return HttpResponse(status=404)
    try:
        orders_obj = Order.objects.filter(user_profile=user_profile)
    except Order.DoesNotExist:
         return HttpResponse(status=404)
    orders = GetOrderSerializer(orders_obj,many=True)
    return Response(orders.data)