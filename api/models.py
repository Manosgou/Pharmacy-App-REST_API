from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    PHARMACIST='PH'
    SUPPLIER='SP'
    CUSTOMER='CU'
    DOMAIN=[
        (PHARMACIST,'Pharmacist'),
        (SUPPLIER,'Supplier'),
        (CUSTOMER,'Customer')

        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=2,choices=DOMAIN,default=PHARMACIST)

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
     instance.userprofile.save()

class MedicineCategory(models.Model):
    name = models.CharField(max_length=20)


    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=20)
    quantity = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(MedicineCategory,on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name




class Location(models.Model):
    street = models.CharField(null=True,max_length=30)
    street_num = models.IntegerField(null=True)
    city = models.CharField(null=True,max_length=30)
    postal_code = models.IntegerField(null=True)
    user_profile = models.OneToOneField(UserProfile,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.street or self.user_profile.user.username

class Order(models.Model):
    ON_PROCESS='OP'
    ON_DELIVERY='OD'
    DELIVERED='DE'
    STATUS=[
        (ON_PROCESS,'On Process'),
        (ON_DELIVERY,'On Delivery'),
        (DELIVERED,'Delivered')
    ]

    user_profile = models.ForeignKey(UserProfile,null=True,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)
    total_price = models.FloatField(null=True)
    location = models.ForeignKey(Location,null=True,on_delete=models.SET_NULL)
    order_status= models.CharField(max_length=2,choices=STATUS,default=ON_PROCESS)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: "+str(self.user_profile) +" "+ self.medicine.name+" "+str(self.medicine.quantity)
    
