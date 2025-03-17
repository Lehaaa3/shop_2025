from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm
from users.services import greeting_email


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        greeting_email(username, email)
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
