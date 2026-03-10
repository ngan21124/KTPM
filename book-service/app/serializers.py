from rest_framework import serializers
from .models import Book, Promotion, Voucher

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'