from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, DeleteView

from catalog.services import send_mail_from_contact
from catalog.forms import ProductForm
from catalog.models import Product, Contacts


class ProductListView(ListView):
    model = Product
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Главная'

        return context_data


class ContactView(LoginRequiredMixin, TemplateView):
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
            send_mail_from_contact(name, phone, message)
            print(f"{name}, {phone}, {message}")
            return redirect(reverse('catalog:contact'))


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = obj.name
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:product_list')
