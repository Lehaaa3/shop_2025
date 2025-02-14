from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import main, contact, product_detail, ProductCreateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', main, name='main'),
    path('contact/', contact, name='contact'),
    path('details/<int:pk>/', product_detail, name='product_detail'),
    path('products/create', ProductCreateView.as_view(), name='create_product'),
]
