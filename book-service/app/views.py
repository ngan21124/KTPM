from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Promotion, Voucher
from .serializers import BookSerializer, PromotionSerializer, VoucherSerializer

class BookListCreate(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    """Chi tiết sách"""
    
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PromotionListCreate(APIView):
    """Quản lý khuyến mãi"""
    
    def get(self, request):
        promotions = Promotion.objects.all()
        serializer = PromotionSerializer(promotions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoucherListCreate(APIView):
    """Quản lý voucher"""
    
    def get(self, request):
        vouchers = Voucher.objects.all()
        serializer = VoucherSerializer(vouchers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VoucherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)