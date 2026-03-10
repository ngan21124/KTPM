from django.urls import path
from .views import CartCreate, AddCartItem, ViewCart, GetOrCreateCart, CartItemList

urlpatterns = [
    path('carts/', CartCreate.as_view()),
    path('carts/<int:customer_id>/', GetOrCreateCart.as_view()),
    path('carts/<int:customer_id>/items/', CartItemList.as_view()),
    path('carts/<int:customer_id>/items/add/', AddCartItem.as_view()),
]
