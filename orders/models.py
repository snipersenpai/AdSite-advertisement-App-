from django.db import models
from ads.models import *

class Order(models.Model):
    first_name  = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: No.{self.pk}, by {self.first_name} {self.last_name} ({self.email}), placed on {self.created} |  {self.items.count()} total items | total:${self.get_total_cost()} | address {self.address} {self.postal_code} {self.city} | paid {self.paid}"
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'Order ({self.id}): {self.ad.title}, {self.quantity} item(s). ${self.get_cost()}'
    def get_cost(self):
        return self.price*self.quantity
