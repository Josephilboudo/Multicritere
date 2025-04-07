from django import template

register = template.Library()

@register.filter
def get_dict_item(dictionary, key):
    """
    Récupère un élément de dictionnaire de manière sécurisée.
    Retourne la valeur ou une chaîne vide si la clé n'existe pas.
    """
    return dictionary.get(key, "")