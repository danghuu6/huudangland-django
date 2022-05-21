from django.db import models
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255, default='')
    price = models.IntegerField(default=0, null=True)
    area = models.FloatField(default=0.0)
    address = models.CharField(max_length=255, default='')
    location_house = models.IntegerField(default=0)
    floors = models.IntegerField(default=0)
    to_center = models.FloatField(default=0.0)
    image = models.TextField(default='')
    price_predict = models.IntegerField(default=0, null=True)
    time = models.DateTimeField(auto_now=True)
