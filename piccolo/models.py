from django.db import models

# Create your models here.
""" Will be using three models Buyer model and Transaction Model
    Buyer Model - first_name, last_name,phone,buyer_id
    Transaction model - buyer_id(foreign_key),product_id,count
    PreviousOrders model - order_id(this will store old orders, so that if Webhook post request is repeated,transaction models count does not increase)
"""


class Buyers(models.Model):
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    buyer_id = models.IntegerField(unique=True, blank=False)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class PreviousOrders(models.Model):
    order_id = models.IntegerField(max_length=20, unique=True)

    def __unicode__(self):
        return str(self.order_id)


class Transactions(models.Model):
    buyer_id = models.IntegerField(blank=False)
    product_id = models.IntegerField(blank=False)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.count)