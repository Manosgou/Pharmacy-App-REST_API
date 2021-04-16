from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Employee(models.Model):
    PHARMACIST='PH'
    SUPPLIER='SP'
    DOMAIN=[
        (PHARMACIST,'Pharmacist'),
        (SUPPLIER,'Supplier')
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=2,choices=DOMAIN,default=PHARMACIST)

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_employee(sender, instance, **kwargs):
     instance.employee.save()