from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post
from blog.utils import get_avail_post_by_id


class PostOneMixin:
    """Класс с общими параметрами постов."""

    model = Post


class PostIdMixin(PostOneMixin):
    """Класс с ID для редактирования/удаления."""

    pk_url_kwarg = 'post_id'

    def get_object(self):
        return get_avail_post_by_id(
            self.request.user.username,
            self.kwargs['post_id']
        )


class PostFormMixin(PostOneMixin):
    """Класс с формой постов."""

    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostChangesMixin(PostIdMixin, PostFormMixin):
    """Класс с общими параметрами и проверками для изменения постов."""

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostForm(instance=get_object_or_404(
            Post, id=self.kwargs['post_id']))
        context['form'] = form
        return context


class CommentMixin:
    """Класс с общими параметрами для комментариев."""

    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])


class CommentAuthCheckMixin(CommentMixin):
    """Класс с параметром ID и проверкой автора комментария."""

    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return redirect(
                'blog:post_detail', post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)
