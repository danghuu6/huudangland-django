from django.db import models
from product.models import Product
from customer.models import Customer
# Create your models here.


class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    content = models.TextField(default='')
    tel_contact = models.CharField(default='', max_length=10, null=True)
    time = models.DateTimeField(auto_now=True)