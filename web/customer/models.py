from django.db import models


# Create your models here.


class Customer(models.Model):
    phone_number = models.CharField(max_length=10, default='', primary_key=True)
    name_customer = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=20, null=False, default='')
    date_of_birth = models.CharField(max_length=10, default='')
    gt = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

