from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Customer, User
from .serializers import CustomerSerializer, UserSerializer
import requests
import json

CART_SERVICE_URL = "http://cart-service:8000"

class LoginView(APIView):
    """API endpoint để đăng nhập"""
    
    def post(self, request):
        try:
            data = request.data if hasattr(request, 'data') else json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Xác thực người dùng
            user = authenticate(username=username, password=password)
            
            if user is not None:
                return Response({
                    'success': True,
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': getattr(user, 'role', 'customer'),
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Username hoặc mật khẩu không đúng'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    """API endpoint để đăng ký"""
    
    def post(self, request):
        try:
            # Sử dụng UserSerializer để tạo user
            serializer = UserSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'success': True,
                    'id': user.id,
                    'message': 'Đăng ký thành công'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomerListCreate(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()

            # call cart service
            requests.post(
                f"{CART_SERVICE_URL}/carts/",
                json={"customer_id": customer.id}
            )

            return Response(serializer.data)

        return Response(serializer.errors)