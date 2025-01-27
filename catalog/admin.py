from django.contrib import admin

from catalog.models import Product, Category, Contacts


@admin.register(Category)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Product)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Contacts)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'country', 'address', 'INN')
    list_filter = ('country',)
