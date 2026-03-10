#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')
django.setup()

from django.contrib.auth import get_user_model
from book_service.app.models import Book, Promotion, Voucher
from customer_service.app.models import User as CustomerUser

User = get_user_model()

# Create sample books
books_data = [
    {'title': 'Python Cơ Bản', 'author': 'Nguyễn Văn A', 'description': 'Hướng dẫn Python cho người mới bắt đầu', 'price': 150000, 'stock': 20},
    {'title': 'Django Advanced', 'author': 'Trần Thị B', 'description': 'Lập trình Django nâng cao', 'price': 250000, 'stock': 15},
    {'title': 'Web Development', 'author': 'Lê Văn C', 'description': 'Phát triển web với HTML, CSS, JavaScript', 'price': 200000, 'stock': 25},
    {'title': 'Microservices Architecture', 'author': 'Phạm Văn D', 'description': 'Kiến trúc Microservices trong thực tế', 'price': 350000, 'stock': 10},
    {'title': 'Database Design', 'author': 'Vũ Thị E', 'description': 'Thiết kế cơ sở dữ liệu hiệu quả', 'price': 220000, 'stock': 18},
]

print("Creating sample books...")
for book_data in books_data:
    book, created = Book.objects.get_or_create(
        title=book_data['title'],
        defaults={
            'author': book_data['author'],
            'description': book_data['description'],
            'price': book_data['price'],
            'stock': book_data['stock'],
        }
    )
    if created:
        print(f"✓ Created: {book.title}")
    else:
        print(f"→ Already exists: {book.title}")

# Create sample promotions
print("\nCreating sample promotions...")
books = Book.objects.all()[:3]
today = datetime.now().date()
for i, book in enumerate(books):
    promo, created = Promotion.objects.get_or_create(
        book=book,
        defaults={
            'discount_percent': 10 + (i * 5),
            'start_date': today,
            'end_date': today + timedelta(days=30),
        }
    )
    if created:
        print(f"✓ Created promotion for: {book.title}")
    else:
        print(f"→ Already exists for: {book.title}")

# Create sample vouchers
print("\nCreating sample vouchers...")
vouchers_data = [
    {'code': 'SAVE10', 'discount_percent': 10, 'max_uses': 100},
    {'code': 'SAVE20', 'discount_percent': 20, 'max_uses': 50},
    {'code': 'VIP30', 'discount_percent': 30, 'max_uses': 10},
]

for voucher_data in vouchers_data:
    voucher, created = Voucher.objects.get_or_create(
        code=voucher_data['code'],
        defaults={
            'discount_percent': voucher_data['discount_percent'],
            'max_uses': voucher_data['max_uses'],
            'used_count': 0,
            'start_date': today,
            'end_date': today + timedelta(days=90),
        }
    )
    if created:
        print(f"✓ Created voucher: {voucher.code}")
    else:
        print(f"→ Already exists: {voucher.code}")

print("\n✅ Sample data created successfully!")
