from app.models import Book, Promotion, Voucher
from datetime import datetime, timedelta

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
        defaults=book_data
    )
    print(f"{'✓' if created else '→'} {book.title}")

print("\nCreating sample vouchers...")
vouchers_data = [
    {'code': 'SAVE10', 'discount_percent': 10, 'max_uses': 100},
    {'code': 'SAVE20', 'discount_percent': 20, 'max_uses': 50},
    {'code': 'VIP30', 'discount_percent': 30, 'max_uses': 10},
]

today = datetime.now().date()
for voucher_data in vouchers_data:
    voucher_data.update({
        'used_count': 0,
        'start_date': today,
        'end_date': today + timedelta(days=90),
    })
    voucher, created = Voucher.objects.get_or_create(
        code=voucher_data['code'],
        defaults=voucher_data
    )
    print(f"{'✓' if created else '→'} {voucher.code}")

print("\n✅ Sample data created!")
