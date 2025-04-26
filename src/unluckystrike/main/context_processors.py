from blog.models import Category

def blog_categories(request):
    """
    Returns all blog categories to be available in all templates.
    """
    return {
        'blog_categories': Category.objects.all()
    }