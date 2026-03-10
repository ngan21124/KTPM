from django.urls import path
from .views import CustomerListCreate, LoginView, RegisterView

urlpatterns = [
    path('customers/', CustomerListCreate.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
]