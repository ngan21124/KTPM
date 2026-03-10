from app.models import User

# Create test users
users_data = [
    {'username': 'admin', 'email': 'admin@bookstore.com', 'password': 'admin123', 'role': 'admin'},
    {'username': 'staff1', 'email': 'staff@bookstore.com', 'password': 'staff123', 'role': 'staff'},
    {'username': 'customer1', 'email': 'customer@bookstore.com', 'password': 'customer123', 'role': 'customer'},
    {'username': 'customer2', 'email': 'customer2@bookstore.com', 'password': 'customer123', 'role': 'customer'},
]

print('Creating test users...')
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'role': user_data['role'],
            'is_staff': user_data['role'] in ['staff', 'admin'],
            'is_superuser': user_data['role'] == 'admin',
        }
    )
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f"✓ Created {user_data['role']}: {user_data['username']}")
    else:
        print(f"→ Already exists: {user_data['username']}")

print('✅ Test users created!')
