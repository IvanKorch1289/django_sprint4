from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from blog.constants import CNT_POSTS_FOR_PAGINATE
from blog.forms import CommentForm, ProfileForm
from blog.mixins import (CommentAuthCheckMixin, CommentMixin, PostChangesMixin,
                         PostFormMixin, PostIdMixin, PostOneMixin)
from blog.models import Category, Post, User
from blog.utils import get_all_author_posts, get_all_pub_posts


class BasePostListView(PostOneMixin, ListView):
    """Базовый CBV для страниц с постами."""

    paginate_by = CNT_POSTS_FOR_PAGINATE

    def get_queryset(self) -> QuerySet:
        return get_all_pub_posts()


class PostListView(BasePostListView):
    """Представление главной страницы."""

    template_name = 'blog/index.html'


class PostCreateView(LoginRequiredMixin, PostFormMixin, CreateView):
    """Представление для создания объекта поста."""

    def form_valid(self, form):
        form.instance.author = get_object_or_404(User, id=self.request.user.id)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostChangesMixin, UpdateView):
    """Представление для редактирования объекта поста."""

    pass


class PostDeleteView(LoginRequiredMixin, PostChangesMixin, DeleteView):
    """Представление для удаления объекта поста."""

    pass


class PostDetailView(LoginRequiredMixin, PostIdMixin, DetailView):
    """Представление для отображения отдельного объекта поста."""

    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.get_object().comments.all()
        return context


class ProfilePostListView(BasePostListView):
    """Представление для отображения профиля пользователя."""

    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet:
        return get_all_author_posts(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя."""

    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class CategoryPostListView(BasePostListView):
    """Представление для отображения страницы категории постов."""

    slug_url_kwarg = 'category_slug'
    template_name = 'blog/category.html'

    def get_object(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self) -> QuerySet:
        category = self.get_object()
        return super().get_queryset().filter(category__slug=category.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """Представление для создания комментария к посту."""

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post, id=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentAuthCheckMixin, UpdateView):
    """Представление для редактирования комментария к посту."""

    pass


class CommentDeleteView(LoginRequiredMixin, CommentAuthCheckMixin, DeleteView):
    """Представление для удаления комментария к посту."""

    pass
