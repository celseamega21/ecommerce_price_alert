from rest_framework import serializers
from .models import Product, PriceHistory

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PriceHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'