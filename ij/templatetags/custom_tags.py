# templatetags/__init__.py
# Laisser ce fichier vide, il indique à Python que c'est un package

# templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)