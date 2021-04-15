from django.db import models
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

