#!/usr/bin/env python

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_service.settings')
django.setup()

from app.models import Book, Voucher
from decimal import Decimal

# Create sample books
books_data = [
    {
        'title': 'Python Cơ Bản',
        'author': 'Nguyễn Văn A',
        'description': 'Hướng dẫn lập trình Python từ cơ bản đến nâng cao',
        'price': Decimal('150.00'),
        'stock': 50
    },
    {
        'title': 'Django Advanced',
        'author': 'Trần Thị B',
        'description': 'Phát triển web với Django framework',
        'price': Decimal('250.00'),
        'stock': 30
    },
    {
        'title': 'Web Development',
        'author': 'Lê Văn C',
        'description': 'Học web development từ HTML, CSS đến JavaScript',
        'price': Decimal('200.00'),
        'stock': 40
    },
    {
        'title': 'Microservices Architecture',
        'author': 'Phạm Văn D',
        'description': 'Kiến trúc microservices cho ứng dụng hiện đại',
        'price': Decimal('350.00'),
        'stock': 20
    },
    {
        'title': 'Database Design',
        'author': 'Hoàng Văn E',
        'description': 'Thiết kế cơ sở dữ liệu hiệu quả',
        'price': Decimal('220.00'),
        'stock': 25
    }
]

# Create books
for data in books_data:
    book, created = Book.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    status = "✓ created" if created else "- already exists"
    print(f"{status}: {book.title}")

# Create vouchers
from django.utils import timezone
from datetime import timedelta

now = timezone.now()
start_date = now
end_date = now + timedelta(days=30)

vouchers_data = [
    {'code': 'SAVE10', 'discount_percent': 10, 'max_uses': 100},
    {'code': 'SAVE20', 'discount_percent': 20, 'max_uses': 50},
    {'code': 'VIP30', 'discount_percent': 30, 'max_uses': 10},
]

for data in vouchers_data:
    voucher, created = Voucher.objects.get_or_create(
        code=data['code'],
        defaults={
            'discount_percent': data['discount_percent'],
            'max_uses': data['max_uses'],
            'start_date': start_date,
            'end_date': end_date
        }
    )
    status = "✓ created" if created else "- already exists"
    print(f"{status}: {voucher.code}")

print(f"\n📊 Total books: {Book.objects.count()}")
print(f"📊 Total vouchers: {Voucher.objects.count()}")
