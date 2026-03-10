#!/usr/bin/env python3
"""
Test role-based login and redirection
"""
import requests

BASE_URL = "http://localhost:8000"

def test_role_login(username, password, expected_role):
    print(f"\n{'='*60}")
    print(f"Testing {username.upper()} Login (Role: {expected_role.upper()})")
    print(f"{'='*60}")
    
    session = requests.Session()
    
    # Get login page
    response = session.get(f"{BASE_URL}/login/", timeout=5)
    
    # Extract CSRF token
    import re
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = match.group(1) if match else None
    
    if not csrf_token:
        print("[ERROR] CSRF Token not found")
        return False
    
    print("[OK] CSRF Token extracted")
    
    # Submit login
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(f"{BASE_URL}/login/", data=login_data, timeout=5, allow_redirects=True)
    print(f"[OK] Login submitted, status: {response.status_code}")
    print(f"[OK] Final URL: {response.url}")
    
    # Check redirect based on role
    if expected_role == 'admin':
        if 'admin_dashboard' in response.url or '/admin' in response.url:
            print(f"[SUCCESS] Admin dashboard redirected!")
            return True
        else:
            print(f"[FAILED] Expected admin dashboard, got: {response.url}")
            return False
    
    elif expected_role == 'staff':
        if 'staff_dashboard' in response.url or '/staff' in response.url:
            print(f"[SUCCESS] Staff dashboard redirected!")
            return True
        else:
            print(f"[FAILED] Expected staff dashboard, got: {response.url}")
            return False
    
    elif expected_role == 'customer':
        if '/books/' in response.url:
            print(f"[SUCCESS] Books page (customer) redirected!")
            return True
        else:
            print(f"[FAILED] Expected books page, got: {response.url}")
            return False

# Test all three roles
results = {
    'admin': test_role_login('admin', 'admin123', 'admin'),
    'staff': test_role_login('staff1', 'staff123', 'staff'),
    'customer': test_role_login('customer1', 'customer123', 'customer'),
}

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
for role, success in results.items():
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status}: {role.upper()}")
