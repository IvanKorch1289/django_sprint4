from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок')

    class Meta:
        abstract = True


class Category(BaseModel, TitleModel):
    description = models.TextField(
        verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        null=False,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location (BaseModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(BaseModel, TitleModel):
    text = models.TextField(
        verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'))
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_posts',
        verbose_name='Автор публикации',
        null=True)
    location = models.ForeignKey(
        to=Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='location_posts',
        verbose_name='Местоположение')
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_posts',
        verbose_name='Категория')
    image = models.ImageField(
        blank=True,
        upload_to='birthdays_images',
        verbose_name='Фото')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария')
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        null=True,
        related_name='post_comments',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments',
        verbose_name='Автор комментария',
        null=True)

    class Meta:
        ordering = ('created_at',)
