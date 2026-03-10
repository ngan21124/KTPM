from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Books & Search
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Cart & Checkout
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    
    # Staff Management
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/books/', views.manage_books, name='manage_books'),
    path('staff/books/add/', views.add_book, name='add_book'),
    path('staff/books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('staff/books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('staff/promotions/', views.manage_promotions, name='manage_promotions'),
    path('staff/vouchers/', views.manage_vouchers, name='manage_vouchers'),
    
    # Admin Reports
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/reports/book-revenue/', views.book_revenue_report, name='book_revenue_report'),
    path('admin/reports/customers/', views.customer_statistics, name='customer_statistics'),
]
