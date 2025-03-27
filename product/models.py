from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField(max_length=500, unique=True)
    last_price = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.last_price}"
    
class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']