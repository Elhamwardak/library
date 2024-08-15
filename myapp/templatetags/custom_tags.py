from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag("category.html")
def get_categories():
    return {
        'categories': Category.objects.all()
    }