#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_service.settings')
django.setup()

from app.models import User

# Create test users
users_data = [
    {'username': 'admin', 'email': 'admin@bookstore.com', 'password': 'admin123', 'role': 'admin'},
    {'username': 'staff1', 'email': 'staff@bookstore.com', 'password': 'staff123', 'role': 'staff'},
    {'username': 'customer1', 'email': 'customer@bookstore.com', 'password': 'customer123', 'role': 'customer'},
    {'username': 'customer2', 'email': 'customer2@bookstore.com', 'password': 'customer123', 'role': 'customer'},
]

for data in users_data:
    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role']
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'role': role}
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"[CREATED] {username} ({role})")
    else:
        print(f"[EXISTS] {username} ({role})")

print(f"\nTotal users: {User.objects.count()}")
