from django.contrib import admin
from blog.models import Post, Category


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_field = ('status',)
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)