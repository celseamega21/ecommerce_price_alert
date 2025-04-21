from django.contrib import admin
from django.urls import path
from product.views import ProductListCreateView, ProductUpdateDeleteView, index

urlpatterns = [
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:id>/', ProductUpdateDeleteView.as_view(), name='product-update-delete'),
    path('', index, name='home'),
    path('admin/', admin.site.urls),
]