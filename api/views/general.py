from typing import Counter
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import LocationSerializer, UserProfileSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.models import Location,Order,Medicine,UserProfile,MedicineCategory


# Create your views here.


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_profile = UserProfile.objects.get(user=user)
        return Response({
            'token': token.key,
            'domain': user_profile.domain,
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
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    user = UserProfileSerializer(current_user_profile)
    data['user_profile'] = user.data
    if current_user_profile.domain == 'PH':
        obj,created = Location.objects.get_or_create(user_profile=current_user_profile)
        if created: 
            obj.street=''
            obj.street_num=0
            obj.city=''
            obj.postal_code=0
            obj.save()
        medicines_quantity=[]
        deficit_medicines=[]
        for m in Medicine.objects.filter(created_by=current_user_profile):
            item={m.name:m.quantity}
            medicines_quantity.append(item)
            if m.quantity<5:
                deficit_medicines.append(m.name)
        data['deficit_medicines']=deficit_medicines
        data['medicines_quantity']=medicines_quantity
        orders_on_process=Order.objects.filter(user_profile__in=UserProfile.objects.filter(domain='CU'),order_status='OP').count()
        orders_on_deliver = Order.objects.filter(user_profile__in=UserProfile.objects.filter(domain='CU'),order_status='OD').count()
        orders_delivered = Order.objects.filter(user_profile__in=UserProfile.objects.filter(domain='CU'),order_status='DE').count()
        data['orders'] = {'orders_on_process':orders_on_process,'orders_on_deliver':orders_on_deliver,'orders_delivered':orders_delivered}
        location = LocationSerializer(obj)
        data['location'] = location.data
    elif current_user_profile.domain == 'SP':
        last_order = Order.objects.last()
        if last_order is None:
            data['last_order'] = None
        else:
            data['last_order'] = {"full_name":last_order.user_profile.user.first_name+" "+last_order.user_profile.user.last_name,"medicine":last_order.medicine.name,"quantity":last_order.quantity,"total_price":last_order.total_price}
        last_medicine = Medicine.objects.last()
        if last_medicine is None:
            data['last_medicine'] = None
        else:
            data['last_medicine'] ={"name":last_medicine.name,"category":last_medicine.category.name,"quantity":last_medicine.quantity,"price":last_medicine.price}
        data['total_orders']=Order.objects.all().count()
        data['total_medicines']=Medicine.objects.filter(created_by=current_user_profile).count()
        data['total_categories']=MedicineCategory.objects.all().count()
        medicines_quantity=[]
        for m in Medicine.objects.filter(created_by=current_user_profile):
            item={m.name:m.quantity}
            medicines_quantity.append(item)
        data['medicines_quantity']=medicines_quantity
    elif current_user_profile.domain =='CU':
        obj,created = Location.objects.get_or_create(user_profile=current_user_profile)
        if created:
            obj.street=''
            obj.street_num=0
            obj.city=''
            obj.postal_code=0
            obj.save()
        last_order = Order.objects.filter(user_profile=current_user_profile).last()
        if last_order is None:
            data['last_order'] =None
        else:
            data['last_order'] = {"medicine":last_order.medicine.name,"quantity":last_order.quantity,"total_price":last_order.total_price}
        location = LocationSerializer(obj)
        data['location'] = location.data
    return JsonResponse(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def location_update(request,id):
    if request.method =='PUT':
        try:
            user_profile = UserProfile.objects.get(id=id)
            location,created = Location.objects.get_or_create(user_profile=user_profile)
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
        except User.DoesNotExist:
            return HttpResponse(status=404) 
        data = JSONParser().parse(request)
        serializer = UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success':'User updated'}, status=201)
        return JsonResponse(serializer.errors, status=400)