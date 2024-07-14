import pytz

from datetime import datetime as dt

from django.db.models import Count

from blog.models import Post, User


def get_all_posts():
    """Функция получения всех постов"""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).order_by(
        '-pub_date'
    ).annotate(comment_count=Count('post_comments'))


def get_all_pub_posts():
    """Функция получения всех опубликованных постов"""
    return get_all_posts().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.now(tz=pytz.UTC))


def get_all_author_posts(username):
    """Функция получения всех постов автора"""
    return get_all_posts().filter(author=User.objects.get(username=username))


def get_avail_posts(username):
    """Функция получения постов с доступными параметрами"""
    return get_all_author_posts(username=username).union(get_all_pub_posts())


def get_avail_post_by_id(username, post_id):
    """Функция проверки доступности поста"""
    post = Post.objects.get(id=post_id)

    check_is_pub = not post.is_published or not post.category.is_published
    check_pub_date = post.pub_date > dt.now(tz=pytz.UTC)

    if post.author.username != username and (check_is_pub or check_pub_date):
        return None
    return post
