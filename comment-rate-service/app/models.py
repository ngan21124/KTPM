from django.db import models

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    book_id = models.IntegerField()
    customer_id = models.IntegerField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for Book {self.book_id} - Rating {self.rating}"
