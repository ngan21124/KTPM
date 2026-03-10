from django.urls import path
from .views import BookListCreate, BookDetail, PromotionListCreate, VoucherListCreate

urlpatterns = [
    path('books/', BookListCreate.as_view()),
    path('books/<int:book_id>/', BookDetail.as_view()),
    path('promotions/', PromotionListCreate.as_view()),
    path('vouchers/', VoucherListCreate.as_view()),
]