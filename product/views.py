from .serializers import ProductSerializers, PriceHistorySerializers
from .models import PriceHistory, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .scrape import Scrape

class ProductView(APIView):
    def get(self, request):
        """Get all products tracked"""
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Add products to price tracking system"""
        product_name = request.data.get("product_name")
        email = request.data.get("email")
        if not product_name or not email:
            return Response({"error": "Product name and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        # scrape product
        scraper = Scrape(product_name).scrape_tokped()
        if not scraper:
            return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_url = scraper.get("product_url")
        if not product_url:
            return Response({"error": "Product URL not found"}, status=status.HTTP_400_BAD_REQUEST)

        # save data product to database
        product, created = Product.objects.update_or_create(
            url=scraper["product_url"], 
            defaults={"name": scraper["product_name"], "last_price": scraper["discount_price"], "email": email})
        
        # save price to database
        PriceHistory.objects.create(product=product, price=scraper["discount_price"])

        serializer = ProductSerializers(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)