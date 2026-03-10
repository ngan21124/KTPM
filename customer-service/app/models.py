from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Extended user model with roles"""
    ROLE_CHOICES = [
        ('customer', 'Khách hàng'),
        ('staff', 'Nhân viên'),
        ('admin', 'Quản trị viên'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Customer(models.Model):
    """Customer profile linked to User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username