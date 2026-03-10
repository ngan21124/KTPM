#!/usr/bin/env python3
"""
Final verification test - books display and add book functionality
"""
import requests
import re

BASE_URL = "http://localhost:8000"
BOOK_SERVICE = "http://localhost:8002"

print("="*60)
print("SYSTEM VERIFICATION TEST")
print("="*60)

# Test 1: Book Service API has books
print("\n[TEST 1] Book Service API")
try:
    resp = requests.get(f"{BOOK_SERVICE}/books/", timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        books = data.get('value', data if isinstance(data, list) else [])
        print(f"[OK] Books in API: {len(books)}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 2: Books display on web page
print("\n[TEST 2] Book Display on Web")
try:
    resp = requests.get(f"{BASE_URL}/books/", timeout=5)
    if resp.status_code == 200:
        if "Python" in resp.text or "Django" in resp.text:
            print("[OK] Books are displaying on web page")
        else:
            print("[WARNING] Books might not be rendering")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 3: Staff can login
print("\n[TEST 3] Staff Login & Add Book Page")
session = requests.Session()
try:
    # Get CSRF token
    resp = session.get(f"{BASE_URL}/login/", timeout=5)
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
    csrf = match.group(1) if match else None
    
    if csrf:
        # Login
        login_data = {
            'username': 'staff1',
            'password': 'staff123',
            'csrfmiddlewaretoken': csrf
        }
        resp = session.post(f"{BASE_URL}/login/", data=login_data, timeout=5, allow_redirects=True)
        
        if '/staff/dashboard/' in resp.url:
            print("[OK] Staff logged in successfully")
            
            # Try to access add book page
            resp = session.get(f"{BASE_URL}/staff/books/add/", timeout=5)
            if resp.status_code == 200:
                print("[OK] Add book page accessible")
            else:
                print(f"[WARNING] Add book page returned {resp.status_code}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 4: Admin Dashboard
print("\n[TEST 4] Admin Login & Dashboard")
session = requests.Session()
try:
    # Get CSRF token
    resp = session.get(f"{BASE_URL}/login/", timeout=5)
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
    csrf = match.group(1) if match else None
    
    if csrf:
        # Login
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'csrfmiddlewaretoken': csrf
        }
        resp = session.post(f"{BASE_URL}/login/", data=login_data, timeout=5, allow_redirects=True)
        
        if '/admin/dashboard/' in resp.url:
            print("[OK] Admin logged in successfully")
        else:
            print(f"[WARNING] Admin redirected to {resp.url}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 5: Customer Shopping
print("\n[TEST 5] Customer Login & Shop")
session = requests.Session()
try:
    # Get CSRF token
    resp = session.get(f"{BASE_URL}/login/", timeout=5)
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
    csrf = match.group(1) if match else None
    
    if csrf:
        # Login
        login_data = {
            'username': 'customer1',
            'password': 'customer123',
            'csrfmiddlewaretoken': csrf
        }
        resp = session.post(f"{BASE_URL}/login/", data=login_data, timeout=5, allow_redirects=True)
        
        if '/books/' in resp.url:
            print("[OK] Customer logged in and viewing books")
        else:
            print(f"[WARNING] Customer redirected to {resp.url}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
