from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('details/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create', ProductCreateView.as_view(), name='create_product'),
    path('products/update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('products/delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product')
]
