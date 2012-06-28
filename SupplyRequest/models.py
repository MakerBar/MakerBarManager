from django.db import models
from django.contrib.auth.models import User
#from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User,unique=True)

    def __unicode__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField('Name',max_length=50)
    web_site_domain = models.URLField('Domain URL',max_length=50)

    def __unicode__(self):
        return self.name
class Order_Request(models.Model):
    requestor = models.ForeignKey(User,unique=True)
    request_date = models.DateField('Request Date')
    request_placed = models.BooleanField('Time Sensitive')

    def __unicode__(self):
        return 'Order %d' % (self.id)
class Product(models.Model):
    order=models.ForeignKey(Order_Request)
    supplier = models.ForeignKey(Supplier)
    name = models.CharField('Name',max_length=100)
    quantity = models.IntegerField('Quantity')
    part_number = models.CharField('Part Number',max_length=200)
    web_link = models.URLField('URL',max_length=500)
    cost = models.DecimalField('Cost',decimal_places=2,max_digits=6)

    def __unicode__(self):
        return self.name
class Shipment(models.Model):
    STATUS_CHOICES = (
        ('PD','Pending'),
        ('OD','Ordered'),
        ('SP','Shipped'),
        ('AR','Arrived'),
    )
    SHIPPER_CHOICES = (
        ('FX','Fed Ex'),
        ('US','USPS'),
        ('UP','UPS'),
        ('OT','Other'),
    )
    supplier = models.ForeignKey(Supplier)
    product = models.ManyToManyField(Product)
    status = models.CharField('Status',max_length=2,choices=STATUS_CHOICES)
    order_date = models.DateField('Order Date')
    shipper=models.CharField('Shipped By',max_length=2,choices=SHIPPER_CHOICES)
    tracking_number = models.DecimalField('Tracking Number',max_digits=20,decimal_places=0)



