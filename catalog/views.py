from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Contacts


class ProductListView(ListView):
    model = Product
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Главная'
        return context_data


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['contacts'] = Contacts.objects.get(pk=1)
        context_data['title'] = 'Контакты'
        return context_data

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f"{name}, {phone}, {message}")
            return redirect(reverse('catalog:contact'))


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = obj.name
        return context_data


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:product_list')
