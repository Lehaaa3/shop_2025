from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import CreateView

from catalog.forms import ProductForm
from catalog.models import Product, Contacts


def main(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 2)
    page_number = request.GET.get('page')

    context = {
        'title': 'Главная',
        'object_list': products_list,
        'page_obj': paginator.get_page(page_number)

    }
    return render(request, 'catalog/main.html', context)


def contact(request):
    contacts = Contacts.objects.get(pk=1)
    context = {
        'title': 'Контакты',
        'contacts': contacts
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name}, {phone}, {message}")
    return render(request, 'catalog/contact.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'title': product.name,
        'object': product
    }
    return render(request, 'catalog/product_detail.html', context)


class ProductCreateView(CreateView, ProductForm):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:main')
