from django.contrib import admin
from blog.models import Post, Category, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'last_modified')
    list_field = ('status',)
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'last_modified')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_on', 'post')
    search_fileds = ['author', 'body']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)