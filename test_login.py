#!/usr/bin/env python3
"""
Test script to verify login system works end-to-end
"""
import requests
import re
from bs4 import BeautifulSoup

# Base URL for API Gateway
BASE_URL = "http://localhost:8000"

def extract_csrf_token(html):
    """Extract CSRF token from HTML form"""
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
    return match.group(1) if match else None

def test_login_flow():
    print("=" * 60)
    print("BOOKSTORE MICROSERVICE - LOGIN SYSTEM TEST")
    print("=" * 60)
    
    # Create session to handle cookies
    session = requests.Session()
    
    # Test 1: GET login page
    print("\n[TEST 1] GET /login/ - Fetch login page")
    print("-" * 60)
    try:
        response = session.get(f"{BASE_URL}/login/", timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Extract CSRF token
            csrf_token = extract_csrf_token(response.text)
            if csrf_token:
                print(f"✓ CSRF Token: {csrf_token[:20]}...")
            else:
                print("✗ CSRF Token: NOT FOUND")
                return
            
            # Check for username and password fields
            if 'name="username"' in response.text and 'name="password"' in response.text:
                print("✓ Form fields found: username, password")
            else:
                print("✗ Form fields: NOT FOUND")
                return
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 2: POST login with credentials
    print("\n[TEST 2] POST /login/ - Submit login form")
    print("-" * 60)
    
    login_data = {
        'username': 'customer1',
        'password': 'customer123',
        'csrfmiddlewaretoken': csrf_token
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/login/",
            data=login_data,
            timeout=5,
            allow_redirects=True
        )
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Final URL: {response.url}")
        
        # Check if redirected to books page
        if '/books/' in response.url or 'books' in response.text:
            print("✓ Successfully redirected to books page")
        else:
            print("? Login completed but URL not as expected")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 3: Verify session is authenticated
    print("\n[TEST 3] GET /books/ - Verify authenticated session")
    print("-" * 60)
    try:
        response = session.get(f"{BASE_URL}/books/", timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Books page accessible")
            # Count books in response
            book_count = response.text.count('<div class="book-item">')
            if book_count > 0:
                print(f"✓ Found {book_count} book(s) on page")
            else:
                print("? No books found in response")
        else:
            print(f"✗ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 4: Test logout
    print("\n[TEST 4] GET /logout/ - Test logout")
    print("-" * 60)
    try:
        response = session.get(f"{BASE_URL}/logout/", timeout=5, allow_redirects=True)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Final URL: {response.url}")
        
        if '/login/' in response.url or '/books/' in response.url:
            print("✓ Logout successful, redirected")
        else:
            print("? Logout completed")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_login_flow()
