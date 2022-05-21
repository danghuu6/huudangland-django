from django.db import models
from customer.models import Customer
from product.models import Product
# Create your models here.


class Predict(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, default='', null=True)
    area = models.FloatField(default=0.0)
    location_house = models.IntegerField(default=0)
    floors = models.IntegerField(default=0)
    to_center = models.FloatField(default=0.0)
    price_predict = models.IntegerField(default=0)
    email = models.CharField(max_length=255, default='')
    time = models.DateTimeField(auto_now=True)

class Parameter(models.Model):
    parameter_id = models.CharField(max_length=255, null=False, default='', primary_key=True)
    parameter_list = models.CharField(max_length=255, null=False, default='')
    parameter_descriptions = models.TextField(default='')
    parameter_using = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)

