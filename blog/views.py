from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import PostForm
from blog.models import Post
from blog.services import send_mail_to_me


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = 'Блог'
        return context_data


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        if self.object.number_of_views == 100:
            send_mail_to_me(self.object.title)
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_list')


class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_details', args=[self.kwargs.get('pk')])
