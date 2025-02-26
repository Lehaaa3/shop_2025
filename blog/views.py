from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.forms import PostForm
from blog.models import Post
from blog.services import send_mail_to_me


class PostListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = 'Блог'
        return context_data


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        if self.object.number_of_views == 100:
            send_mail_to_me(self.object.title)
        self.object.save()
        return self.object


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_list')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('blog:post_list')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_details', args=[self.kwargs.get('pk')])
