from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model =Location
        fields=['id','street','street_num','city','postal_code']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','last_name','first_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model=UserProfile
        fields=['user','domain']


class MedicineCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    class Meta:
        model = MedicineCategory
        fields=['id','name']



class MedicineSerializer(serializers.ModelSerializer):
        category = MedicineCategorySerializer()
        class Meta:
            model=Medicine
            fields=['id','name','quantity','price','category']

        def create(self, validated_data):
            category = validated_data.pop('category')
            category_instance = MedicineCategory.objects.get(**category)
            medicine_instance = Medicine.objects.create(**validated_data, category=category_instance)
            return medicine_instance
        
        def update(self,instance, validated_data):
            category = validated_data.pop('category')
            instance.name = validated_data.get('name',instance.name)
            instance.quantity = validated_data.get('quantity',instance.quantity)
            instance.price = validated_data.get('price',instance.price)
            instance.category = MedicineCategory.objects.get(**category)
            instance.save()
            return instance



class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['user_profile','medicine','quantity','total_price','location']
        


class GetOrderSerializer(serializers.ModelSerializer):
    medicine=MedicineSerializer()
    class Meta:
        model=Order
        fields=['id','medicine','quantity','total_price','order_status','date_ordered']


class GetAllOrdersSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    medicine=MedicineSerializer()
    location = LocationSerializer()
    class Meta:
        model=Order
        fields=['id','user_profile','medicine','quantity','total_price','location','order_status','date_ordered']

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=['order_status']