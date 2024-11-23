from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ecomeapp.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('out of delivery', 'out of delivery'),
        ('delivered', 'delivered'),
    ]
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id )
    
    def __str__(self):
        return self.product.product_name

class Checkout(models.Model):
    pass