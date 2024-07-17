from django.contrib import admin

from blog.models import Category, Location, Post, Comment


admin.site.empty_value_display = "(None)"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'text',
                    'pub_date',
                    'category',
                    'location',
                    'is_published']
    list_select_related = ['category',
                           'location']
    date_hierarchy = 'created_at'
    list_max_show_all = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'description',
                    'is_published']
    date_hierarchy = 'created_at'
    list_max_show_all = 5
    prepopulated_fields = {'slug': ['slug']}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'is_published']
    date_hierarchy = 'created_at'
    list_max_show_all = 5


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text']
    date_hierarchy = 'created_at'
    list_max_show_all = 5
