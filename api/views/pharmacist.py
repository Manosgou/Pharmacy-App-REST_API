from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers import *
from rest_framework.parsers import JSONParser
from api.models import UserProfile,Medicine,Order
from api.serializers import MedicineSerializer,CreateOrderSerializer,GetOrderSerializer,GetAllOrdersSerializer,OrderStatusSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medicines(request):
    medicines = MedicineSerializer(Medicine.objects.filter(created_by__in=UserProfile.objects.filter(domain='SP')),many=True)
    return Response(medicines.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pharmacist_medicines(request):
    medicines = MedicineSerializer(Medicine.objects.filter(created_by__in=UserProfile.objects.filter(user=request.user)),many=True)
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
    user_profile = UserProfile.objects.get(domain='SP')
    try:
        medicines = MedicineSerializer(Medicine.objects.filter(created_by=user_profile),many=True)
    except Medicine.DoesNotExist:
        return HttpResponse(status=404)
    return Response(medicines.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    try:
        user_profile =  UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse(status=404)
    try:
        orders = GetOrderSerializer(Order.objects.filter(user_profile=user_profile),many=True)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    return Response(orders.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_medicine_available(request,id):
    current_user = request.user
    try:
        current_user_profile = UserProfile.objects.get(user=current_user)
    except UserProfile.DoesNotExist:
        return HttpResponse(status=404)
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    try:
        medicine = Medicine.objects.get(id=order.medicine.id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if Medicine.objects.filter(name=medicine.name,created_by=current_user_profile).exists():
        return JsonResponse({'error':'Το προϊόν είναι ήδη διαθέσιμο'},status=400)
    if request.method =='POST' and current_user_profile.domain =='PH':
        data = JSONParser().parse(request)
        obj = medicine
        obj.pk=None
        obj.quantity=order.quantity
        obj.price = data['price']
        obj.created_by = current_user_profile
        obj.save()
        return JsonResponse({'success':'Medicine is avaialable'},status=201)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine_price(request,id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse(status=404)
    try:
        medicine = Medicine.objects.get(id=id,created_by=user_profile)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='PUT'and user_profile.domain =='PH':
        data = JSONParser().parse(request)
        medicine.price =  data['price']
        medicine.save()
        return JsonResponse({'success':'Medicine price updated'},status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customers_orders(request):
    orders = GetAllOrdersSerializer( Order.objects.filter(user_profile__in=UserProfile.objects.filter(domain='CU')),many=True)
    return Response(orders.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer_order_status(request,id):
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='PUT'and user_profile.domain =='PH':
        data = JSONParser().parse(request)
        serializer = OrderStatusSerializer(order,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_customer_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    if request.method =='DELETE':
        order.delete()
        return HttpResponse(status=204)
