from django.contrib import admin
from blog.models import Post, Category, Location


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
    empty_value_display = "-empty-"
    list_max_show_all = 10


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'description',
                    'is_published']
    date_hierarchy = 'created_at'
    empty_value_display = "-empty-"
    list_max_show_all = 5
    prepopulated_fields = {'slug': ['slug']}


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'is_published']
    date_hierarchy = 'created_at'
    empty_value_display = "-empty-"
    list_max_show_all = 5


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
