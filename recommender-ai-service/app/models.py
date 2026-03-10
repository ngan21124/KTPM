from django.db import models

class Recommendation(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    score = models.FloatField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recommendation for Customer {self.customer_id} - Book {self.book_id}"
