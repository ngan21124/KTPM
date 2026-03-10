from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import requests
import json

BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
CUSTOMER_SERVICE_URL = "http://customer-service:8000"

# ==================== AUTHENTICATION ====================

def register(request):
    """Đăng ký khách hàng mới"""
    if request.user.is_authenticated:
        return redirect('book_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Mật khẩu không khớp!')
            return render(request, 'register.html')
        
        if len(password) < 6:
            messages.error(request, 'Mật khẩu phải có ít nhất 6 ký tự!')
            return render(request, 'register.html')
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username đã tồn tại!')
                return render(request, 'register.html')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email đã tồn tại!')
                return render(request, 'register.html')
            
            # Tạo user trong Customer Service
            try:
                r = requests.post(
                    f"{CUSTOMER_SERVICE_URL}/customers/",
                    json={
                        'username': username,
                        'email': email,
                        'password': password,
                        'phone': phone,
                        'role': 'customer'
                    }
                )
                if r.status_code != 201 and r.status_code != 200:
                    messages.error(request, 'Lỗi tạo tài khoản ở Customer Service')
                    return render(request, 'register.html')
            except:
                pass  # Nếu lỗi, vẫn tạo local
            
            # Tạo user local
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
            )
            
            # Đăng nhập tự động
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Đăng ký thành công!')
                return redirect('book_list')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'register.html')


def login_view(request):
    """Đăng nhập"""
    if request.user.is_authenticated:
        return redirect('book_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Gọi Customer Service để xác thực
            r = requests.post(
                f"{CUSTOMER_SERVICE_URL}/login/",
                json={'username': username, 'password': password}
            )
            
            if r.status_code == 200:
                data = r.json()
                # Tạo hoặc lấy user local
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': data.get('email', f'{username}@bookstore.com'),
                        'first_name': data.get('first_name', ''),
                        'last_name': data.get('last_name', ''),
                    }
                )
                # Đặt mật khẩu để Django có thể xác thực
                user.set_password(password)
                user.save()
                
                # Cập nhật hoặc tạo UserProfile với role
                from gateway.models import UserProfile
                user_role = data.get('role', 'customer')
                profile, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': user_role,
                        'customer_id': data.get('id')
                    }
                )
                # Cập nhật role nếu thay đổi
                if profile.role != user_role:
                    profile.role = user_role
                    profile.customer_id = data.get('id')
                    profile.save()
                
                # Đăng nhập người dùng
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    # Lưu thông tin trong session
                    request.session['customer_id'] = data.get('id')
                    request.session['user_role'] = user_role
                    
                    # Redirect dựa vào role
                    if user_role == 'admin':
                        return redirect('admin_dashboard')
                    elif user_role == 'staff':
                        return redirect('staff_dashboard')
                    else:
                        next_url = request.GET.get('next', 'book_list')
                        return redirect(next_url)
            else:
                messages.error(request, 'Username hoặc mật khẩu không đúng!')
        except Exception as e:
            messages.error(request, f'Lỗi đăng nhập: {str(e)}')
    
    return render(request, 'login.html')


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.success(request, 'Đã đăng xuất!')
    return redirect('book_list')


# ==================== BOOKS & SEARCH ====================

def index(request):
    """Trang chủ"""
    return redirect('book_list')


def book_list(request):
    """Danh sách sách với tìm kiếm"""
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        if r.status_code == 200:
            data = r.json()
            # Handle both array and {value:[...]} response formats
            if isinstance(data, dict) and 'value' in data:
                books = data['value']
            elif isinstance(data, list):
                books = data
            else:
                books = []
        else:
            books = []
        
        # Tìm kiếm
        search_query = request.GET.get('search', '')
        if search_query:
            books = [b for b in books if 
                    search_query.lower() in b.get('title', '').lower() or 
                    search_query.lower() in b.get('author', '').lower()]
    except Exception as e:
        books = []
    
    return render(request, 'book_list.html', {
        'books': books,
        'search_query': request.GET.get('search', ''),
    })


def book_detail(request, book_id):
    """Chi tiết sách"""
    if not request.user.is_authenticated:
        return redirect(f"login?next=/books/{book_id}/")
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}/")
        book = r.json() if r.status_code == 200 else None
    except:
        book = None
    
    if not book:
        messages.error(request, 'Sách không tồn tại!')
        return redirect('book_list')
    
    return render(request, 'book_detail.html', {
        'book': book,
        'customer_id': request.user.id,
    })


# ==================== CART ====================

@login_required(login_url='login')
def add_to_cart(request, book_id):
    """Thêm sách vào giỏ hàng"""
    if request.method != 'POST':
        return redirect('book_detail', book_id=book_id)
    
    quantity = int(request.POST.get('quantity', 1))
    customer_id = request.user.id
    
    try:
        data = {
            'customer_id': customer_id,
            'book_id': book_id,
            'quantity': quantity
        }
        r = requests.post(f"{CART_SERVICE_URL}/carts/{customer_id}/items/", json=data)
        
        if r.status_code in [200, 201]:
            messages.success(request, 'Đã thêm vào giỏ hàng!')
            return redirect('view_cart')
    except:
        pass
    
    messages.error(request, 'Không thể thêm vào giỏ hàng!')
    return redirect('book_detail', book_id=book_id)


@login_required(login_url='login')
def view_cart(request):
    """Xem giỏ hàng"""
    customer_id = request.user.id
    
    try:
        r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/")
        cart_items = r.json() if r.status_code == 200 else []
    except:
        cart_items = []
    
    return render(request, 'cart.html', {
        'items': cart_items,
        'customer_id': customer_id,
    })


@login_required(login_url='login')
def checkout(request):
    """Thanh toán"""
    customer_id = request.user.id
    
    if request.method == 'POST':
        voucher_code = request.POST.get('voucher_code', '')
        
        try:
            r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/")
            cart_items = r.json() if r.status_code == 200 else []
            
            if not cart_items:
                messages.error(request, 'Giỏ hàng trống!')
                return redirect('view_cart')
            
            order_data = {
                'customer_id': customer_id,
                'items': cart_items,
                'voucher_code': voucher_code,
            }
            
            r = requests.post(f"{CART_SERVICE_URL}/orders/", json=order_data)
            if r.status_code in [200, 201]:
                messages.success(request, 'Đặt hàng thành công!')
                return redirect('order_list')
        except:
            messages.error(request, 'Lỗi trong quá trình thanh toán!')
    
    try:
        r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/")
        cart_items = r.json() if r.status_code == 200 else []
    except:
        cart_items = []
    
    return render(request, 'checkout.html', {
        'items': cart_items,
        'customer_id': customer_id,
    })


@login_required(login_url='login')
def order_list(request):
    """Danh sách đơn hàng"""
    customer_id = request.user.id
    
    try:
        r = requests.get(f"{CART_SERVICE_URL}/orders/?customer_id={customer_id}")
        orders = r.json() if r.status_code == 200 else []
    except:
        orders = []
    
    return render(request, 'order_list.html', {
        'orders': orders,
        'customer_id': customer_id,
    })


# ==================== STAFF ====================

@login_required(login_url='login')
def staff_dashboard(request):
    """Bảng điều khiển nhân viên"""
    if request.user.profile.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and 'value' in data:
                total_books = len(data['value'])
            elif isinstance(data, list):
                total_books = len(data)
            else:
                total_books = 0
        else:
            total_books = 0
    except:
        total_books = 0
    
    return render(request, 'staff_dashboard.html', {
        'total_books': total_books,
    })


@login_required(login_url='login')
def manage_books(request):
    """Quản lý sách"""
    if request.user.profile.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and 'value' in data:
                books = data['value']
            elif isinstance(data, list):
                books = data
            else:
                books = []
        else:
            books = []
    except:
        books = []
    
    return render(request, 'manage_books.html', {'books': books})


@login_required(login_url='login')
def add_book(request):
    """Thêm sách"""
    if request.user.profile.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    if request.method == 'POST':
        try:
            data = {
                'title': request.POST.get('title'),
                'author': request.POST.get('author'),
                'description': request.POST.get('description'),
                'price': float(request.POST.get('price')),
                'stock': int(request.POST.get('stock')),
            }
            r = requests.post(f"{BOOK_SERVICE_URL}/books/", json=data)
            
            if r.status_code in [200, 201]:
                messages.success(request, 'Sách đã thêm!')
                return redirect('manage_books')
        except:
            messages.error(request, 'Lỗi!')
    
    return render(request, 'add_book.html')


@login_required(login_url='login')
def edit_book(request, book_id):
    """Sửa sách"""
    if request.user.profile.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}/")
        book = r.json() if r.status_code == 200 else None
    except:
        book = None
    
    if not book:
        messages.error(request, 'Sách không tồn tại!')
        return redirect('manage_books')
    
    if request.method == 'POST':
        try:
            data = {
                'title': request.POST.get('title'),
                'author': request.POST.get('author'),
                'description': request.POST.get('description'),
                'price': float(request.POST.get('price')),
                'stock': int(request.POST.get('stock')),
            }
            r = requests.put(f"{BOOK_SERVICE_URL}/books/{book_id}/", json=data)
            
            if r.status_code in [200, 201]:
                messages.success(request, 'Sách đã cập nhật!')
                return redirect('manage_books')
        except:
            messages.error(request, 'Lỗi!')
    
    return render(request, 'edit_book.html', {'book': book})


@login_required(login_url='login')
def delete_book(request, book_id):
    """Xóa sách"""
    if request.user.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.delete(f"{BOOK_SERVICE_URL}/books/{book_id}/")
        if r.status_code == 204:
            messages.success(request, 'Sách đã xóa!')
        else:
            messages.error(request, 'Lỗi!')
    except:
        messages.error(request, 'Lỗi!')
    
    return redirect('manage_books')


@login_required(login_url='login')
def manage_promotions(request):
    """Quản lý khuyến mãi"""
    if request.user.profile.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/promotions/")
        promotions = r.json() if r.status_code == 200 else []
    except:
        promotions = []
    
    return render(request, 'manage_promotions.html', {'promotions': promotions})


@login_required(login_url='login')
def manage_vouchers(request):
    """Quản lý voucher"""
    if request.user.profile.role not in ['staff', 'admin']:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/vouchers/")
        vouchers = r.json() if r.status_code == 200 else []
    except:
        vouchers = []
    
    if request.method == 'POST':
        try:
            data = {
                'code': request.POST.get('code'),
                'discount_percent': int(request.POST.get('discount_percent')),
                'max_uses': int(request.POST.get('max_uses')),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
            }
            r = requests.post(f"{BOOK_SERVICE_URL}/vouchers/", json=data)
            if r.status_code in [200, 201]:
                messages.success(request, 'Voucher tạo thành công!')
                return redirect('manage_vouchers')
        except:
            messages.error(request, 'Lỗi!')
    
    return render(request, 'manage_vouchers.html', {'vouchers': vouchers})


# ==================== ADMIN ====================

@login_required(login_url='login')
def admin_dashboard(request):
    """Bảng điều khiển admin"""
    if request.user.role != 'admin':
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        total_books = len(r.json()) if r.status_code == 200 else 0
        
        r = requests.get(f"{CUSTOMER_SERVICE_URL}/users/")
        total_users = len(r.json()) if r.status_code == 200 else 0
    except:
        total_books = total_users = 0
    
    return render(request, 'admin_dashboard.html', {
        'total_books': total_books,
        'total_users': total_users,
    })


@login_required(login_url='login')
def book_revenue_report(request):
    """Báo cáo doanh thu sách"""
    if request.user.profile.role != 'admin':
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    # Lấy tất cả đơn hàng và tính doanh thu
    try:
        r = requests.get(f"{CART_SERVICE_URL}/orders/")
        orders = r.json() if r.status_code == 200 else []
    except:
        orders = []
    
    return render(request, 'book_revenue_report.html', {'orders': orders})


@login_required(login_url='login')
def customer_statistics(request):
    """Thống kê khách hàng"""
    if request.user.profile.role != 'admin':
        messages.error(request, 'Bạn không có quyền!')
        return redirect('book_list')
    
    try:
        r = requests.get(f"{CUSTOMER_SERVICE_URL}/users/")
        users = r.json() if r.status_code == 200 else []
        customers = [u for u in users if u.get('role') == 'customer']
    except:
        customers = []
    
    return render(request, 'customer_statistics.html', {'customers': customers})
