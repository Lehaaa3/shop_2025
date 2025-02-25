from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:login')


class ProfilerView(UpdateView):
    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse('catalog:product_list')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance = self.request.user
        return super().form_valid(form)
