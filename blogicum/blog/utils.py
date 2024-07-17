from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from blog.models import Post, User


def get_all_posts():
    """Функция получения всех постов"""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).order_by(
        '-pub_date'
    ).annotate(comment_count=Count('comments'))


def get_all_pub_posts():
    """Функция получения всех опубликованных постов"""
    return get_all_posts().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    )


def get_all_author_posts(username):
    """Функция получения всех постов автора"""
    return get_all_posts().filter(
        author=get_object_or_404(User, username=username))


def get_avail_posts(username):
    """Функция получения постов с доступными параметрами"""
    return get_all_author_posts(username=username).union(get_all_pub_posts())


def get_avail_post_by_id(username, post_id):
    """Функция проверки доступности поста"""
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=username)

    check_is_pub = not post.is_published or not post.category.is_published
    check_pub_date = post.pub_date > timezone.now()

    if post.author.username != username and (check_is_pub or check_pub_date):
        raise Http404
    return post
