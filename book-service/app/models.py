from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Promotion(models.Model):
    """Khuyến mãi sách"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='promotions')
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    def get_discounted_price(self):
        if self.is_active():
            discount = float(self.book.price) * (self.discount_percent / 100)
            return float(self.book.price) - discount
        return float(self.book.price)
    
    def __str__(self):
        return f"Promotion for {self.book.title} - {self.discount_percent}%"

class Voucher(models.Model):
    """Mã giảm giá"""
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_uses = models.IntegerField(default=100)
    used_count = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.start_date <= now <= self.end_date) and (self.used_count < self.max_uses)
    
    def can_use(self):
        return self.is_active()
    
    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"