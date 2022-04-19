from django.db import models
from customer.models import Customer
from product.models import Product
# Create your models here.


class Predict(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    price_predict = models.IntegerField(default=0)