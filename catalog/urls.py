from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import main, contact

app_name = CatalogConfig.name

urlpatterns = [
    path('', main, name='main'),
    path('contact/', contact, name='contact'),
]
