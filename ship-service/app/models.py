from django.db import models

class Shipment(models.Model):
    SHIPMENT_STATUS = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]
    
    order_id = models.IntegerField()
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=SHIPMENT_STATUS, default='pending')
    carrier = models.CharField(max_length=100)
    estimated_delivery = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_number
