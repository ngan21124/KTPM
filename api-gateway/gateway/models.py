from django.db import models
from django.contrib.auth.models import User as DjangoUser

class UserProfile(models.Model):
    """Mở rộng User model để lưu role"""
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    customer_id = models.IntegerField(null=True, blank=True)  # ID từ Customer Service
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name_plural = "User Profiles"
