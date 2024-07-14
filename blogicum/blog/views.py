from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse

from blog.models import Post, Category, Comment, User
from blog.constants import CNT_POSTS_FOR_PAGINATE
from blog.forms import PostForm, CommentForm, ProfileForm
from blog.utils import (get_all_author_posts,
                        get_all_pub_posts,
                        get_avail_post_by_id)


class BasePostListView(ListView):
    """Базовый CBV для страниц с постами"""

    model = Post
    paginate_by = CNT_POSTS_FOR_PAGINATE

    def get_queryset(self) -> QuerySet:
        return get_all_pub_posts()


class PostListView(LoginRequiredMixin, BasePostListView):
    """Представление главной страницы"""

    template_name = 'blog/index.html'


class PostOneMixin:
    """Класс с общими параметрами постов"""

    model = Post


class PostIdMixin(PostOneMixin):
    """Класс с ID для редактирования/удаления"""

    pk_url_kwarg = 'post_id'


class PostFormMixin(PostOneMixin):
    """Класс с формой постов"""

    template_name = 'blog/create.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username}
                       )


class PostChangesMixin(LoginRequiredMixin, PostIdMixin, PostFormMixin):
    """Класс с общими параметрами и проверками для изменения постов"""

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(PostFormMixin, CreateView):
    """Представление для создания объекта поста"""

    def form_valid(self, form):
        form.instance.author = get_object_or_404(User, id=self.request.user.id)
        return super().form_valid(form)


class PostUpdateView(PostChangesMixin, UpdateView):
    """Представление для редактирования объекта поста"""

    pass


class PostDeleteView(PostChangesMixin, DeleteView):
    """Представление для удаления объекта поста"""

    pass


class PostDetailView(PostIdMixin, DetailView):
    """Представление для отображения отдельного объекта поста"""

    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if get_avail_post_by_id(self.request.user.username, post.id) is None:
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            post=self.kwargs['post_id']
        )
        return context


class ProfileMixin:
    """Класс с общими параметрами для профиля"""

    model = User


class ProfilePostListView(ProfileMixin, DetailView):
    """Представление для отображения профиля пользователя"""

    template_name = 'blog/profile.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(get_all_author_posts(
            username=self.kwargs['username']),
            CNT_POSTS_FOR_PAGINATE)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        context['profile'] = self.get_object()
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, ProfileMixin, UpdateView):
    """Представление для редактирования профиля пользователя"""

    form_class = ProfileForm
    template_name = 'blog/user.html'
    paginate_by = CNT_POSTS_FOR_PAGINATE

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class CategoryPostListView(LoginRequiredMixin, BasePostListView):
    """Представление для отображения страницы категории постов"""

    slug_url_kwarg = 'category_slug'
    template_name = 'blog/category.html'

    def get_object(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self) -> QuerySet:
        if self.get_object() is not None:
            return super().get_queryset().filter(
                category__slug=self.kwargs['category_slug'])
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context


class CommentMixin:
    """Класс с общими параметрами для комментариев"""

    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']}
                       )


class CommentAuthCheckMixin(CommentMixin):
    """Класс с параметром ID и проверкой автора комментария"""

    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """Представление для создания комментария к посту"""

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentAuthCheckMixin, UpdateView):
    """Представление для редактирования комментария к посту"""

    pass


class CommentDeleteView(LoginRequiredMixin, CommentAuthCheckMixin, DeleteView):
    """Представление для удаления комментария к посту"""

    pass
