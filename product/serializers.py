from rest_framework import serializers
from .models import Product, PriceHistory

# serializer for input data
class ProductInputSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'email']

# serializer for output data
class ProductOutputSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PriceHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'