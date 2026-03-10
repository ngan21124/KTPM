from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import requests

BOOK_SERVICE_URL = "http://book-service:8000"


class CartCreate(APIView):

    def post(self, request):

        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOrCreateCart(APIView):
    """Lấy giỏ hàng hiện có hoặc tạo mới cho khách hàng"""
    
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
    
    def post(self, request, customer_id):
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CartItemList(APIView):
    """Liệt kê items trong giỏ hàng"""
    
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
    
    def post(self, request, customer_id):
        """Thêm item vào giỏ hàng"""
        try:
            cart, created = Cart.objects.get_or_create(customer_id=customer_id)
            
            book_id = request.data.get("book_id")
            quantity = request.data.get("quantity", 1)
            
            # Kiểm tra sách có tồn tại không
            try:
                r = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}/")
                if r.status_code != 200:
                    return Response(
                        {"error": "Book not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            except:
                return Response(
                    {"error": "Cannot verify book"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Kiểm tra item đã tồn tại trong giỏ không
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                book_id=book_id,
                defaults={'quantity': quantity}
            )
            
            if not item_created:
                cart_item.quantity += int(quantity)
                cart_item.save()
            
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AddCartItem(APIView):

    def post(self, request):

        book_id = request.data.get("book_id")

        try:
            r = requests.get(f"{BOOK_SERVICE_URL}/books/")
            books = r.json()

            if not any(b["id"] == book_id for b in books):
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            pass

        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewCart(APIView):

    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)