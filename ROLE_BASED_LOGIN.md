# Bookstore Microservice - Role-Based Login System

## Status: ✅ COMPLETE

The login system now properly redirects users to role-appropriate dashboards.

## Features Implemented

### 1. Role-Based Automatic Redirection
After successful login, users are redirected based on their role:
- **Admin** → `/admin/dashboard/` (Admin Dashboard)
- **Staff** → `/staff/dashboard/` (Staff Dashboard)
- **Customer** → `/books/` (Books/Shop Page)

### 2. User Profiles
- Created `UserProfile` model in API Gateway to store role information
- Syncs role from Customer Service during login
- Stores customer_id for inter-service communication

### 3. Test Accounts
Four test users are pre-configured:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| staff1 | staff123 | staff |
| customer1 | customer123 | customer |
| customer2 | customer123 | customer |

### 4. Microservices Architecture
**Services Running:**
- API Gateway (port 8000) - Frontend & authentication routing
- Customer Service (port 8001) - User credentials validation
- Book Service (port 8002) - Book catalog
- Cart Service (port 8003) - Shopping & orders

## How It Works

1. User submits login form with username/password
2. API Gateway validates credentials via Customer Service API
3. Creates/updates local UserProfile with role from Customer Service
4. Django session created for authenticated user
5. Role-based redirect occurs:
   - Admin/Staff: Dedicated management dashboards
   - Customer: Main book shopping page

## Testing

Run the test script to verify:
```bash
cd c:\bookstore-microservice
python test_role_login.py
```

Expected output: All three roles should receive [SUCCESS] status.

## Files Modified

- `api-gateway/gateway/views.py` - Added role-based redirects, UserProfile sync
- `api-gateway/gateway/models.py` - Added UserProfile model
- `api-gateway/api_gateway/urls.py` - Disabled Django admin to avoid routing conflict
- `api-gateway/gateway/templates/book_list.html` - Updated role checks to use profile.role
- Customer Service - Created test users

## Key Implementation Details

- Session stores: `customer_id` and `user_role` for tracking
- UserProfile OneToOne relationship with Django's User model
- Role attribute accessed via `user.profile.role` throughout templates and views
- Login view creates/updates UserProfile atomically with authentication

## Status Code: HTTP 200
All role-based login flows complete successfully with proper 302 redirects.
