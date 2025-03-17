from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView

from blog.services import send_mail_to_me, send_mail_from_contact
from catalog.forms import ProductForm
from catalog.models import Product, Contacts


class ProductListView(ListView):
    model = Product
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Главная'

        return context_data

    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        if request.method == 'POST':
            if 'unpublish' in request.POST:
                if not request.user.has_perm('catalog.can_unpublish_product'):
                    return HttpResponseForbidden("У вас нет прав для отмены публикации.")
                product.is_published = Product.UNPUBLISHED
                product.save(update_fields=["is_published"])
            if 'del_prod' in request.POST:
                delete_product = Permission.objects.get(codename='delete_product')
                if product.owner.pk == self.request.user.pk:
                    self.request.user.user_permissions.add(delete_product)
                if not request.user.has_perm('catalog.delete_product'):
                    return HttpResponseForbidden("У вас нет прав для удаления продукта.")
                product.delete()
                self.request.user.user_permissions.remove(delete_product)
            return redirect('catalog:product_list')


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
            send_mail_from_contact(name, phone, message)
            print(f"{name}, {phone}, {message}")
            return redirect(reverse('catalog:contact'))


class ProductDetailView(DetailView):
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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def dispatch(self, request, *args, **kwargs):
        can_change_product = Permission.objects.get(codename='change_product')
        product = self.get_object()
        if product.owner.pk == self.request.user.pk:
            self.request.user.user_permissions.add(can_change_product)
        if not request.user.has_perm('catalog.change_product'):
            return HttpResponseForbidden("У вас нет прав для редактирования продукта.")
        self.request.user.user_permissions.remove(can_change_product)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('catalog:product_list')
