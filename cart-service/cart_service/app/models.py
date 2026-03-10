from django.db import models
from django.utils import timezone

class Cart(models.Model):
    """Giỏ hàng"""
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    """Item trong giỏ hàng"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Order(models.Model):
    """Đơn hàng"""
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('shipped', 'Đã gửi'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]
    customer_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    voucher_code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    """Item trong đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)