from .serializers import ProductInputSerializers, ProductOutputSerializers, PriceHistorySerializers
from .models import PriceHistory, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .scrape import Scrape
from django.shortcuts import render

def index(request):
    context = {
        'description': 'Track your favorite products in Tokopedia and get notification by email when the price is drop!',
        'title': 'Ecommerce Price Tracker'
    }
    return render(request, "index.html", context)

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductInputSerializers
    queryset = Product.objects.all()
    
    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        if email:
            products = Product.objects.filter(email=email)
        else:
            products = Product.objects.none()
        serializer = ProductOutputSerializers(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product_url = request.data.get("url")
        email = request.data.get("email")
        if not product_url or not email:
            return Response({"error": "Product url and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        # scrape product
        scraper = Scrape(product_url).scrape_tokped()
        if not scraper:
            return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

        # save data product to database
        product, created = Product.objects.update_or_create(
            url=product_url, defaults={"name": scraper["product_name"], "last_price": scraper["discount_price"], "email": email}
        )
        
        # save price to database
        PriceHistory.objects.create(product=product, price=scraper["discount_price"])

        serializer = ProductOutputSerializers(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):    
    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductOutputSerializers(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)