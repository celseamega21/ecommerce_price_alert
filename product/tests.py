from django.test import TestCase
from .models import Product, PriceHistory
from django.core import mail

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name='test', url='www.example.com', last_price=2000, email='test@gmail.com')
        self.assertEqual(product.name, 'test')

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            "Harga Turun!",
            "Produkmu sekarang 80rb!",
            "alert@price.com",
            ["user@email.com"]
        )
        self.assertEqual(len(mail.outbox), 1)