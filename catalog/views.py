from django.shortcuts import render

from catalog.models import Product, Contacts


def main(request):
    products_list = Product.objects.all()[:5]
    print(products_list)
    context = {
        'title': 'Главная',
        'object_list': products_list

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
