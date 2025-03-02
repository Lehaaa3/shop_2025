from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView

from catalog.services import send_mail_from_contact, ProductServices
from catalog.forms import ProductForm
from catalog.models import Product, Contacts, Category
from django.core.cache import cache


class ProductListView(ListView):
    model = Product
    paginate_by = 4

    def get_queryset(self):
        queryset = cache.get('my_queryset')
        if not queryset:
            queryset = super().get_queryset().filter(is_published=True)
            cache.set('my_queryset', queryset, 60 * 15)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Главная'
        context_data['categories'] = Category.objects.all()

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


@method_decorator(cache_page(60 * 15), name='dispatch')
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


@method_decorator(cache_page(60 * 15), name='dispatch')
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


class ProductCategoryView(TemplateView):
    template_name = 'catalog/product_category.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        products = ProductServices().get_products_for_category(category)
        context_data['products'] = products
        context_data['category'] = category

        return context_data
