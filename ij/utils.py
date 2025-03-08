from django.db import connections
from django.conf import settings

def get_dynamic_connection(db_name, user, password):
    """
    Retourne une connexion dynamique à la base de données spécifiée.
    """
    settings.DATABASES[db_name] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': user,  # Remplace par le bon utilisateur MySQL
        'PASSWORD': password,  # Remplace par le bon mot de passe
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'TIME_ZONE': settings.TIME_ZONE,  # Ajout du fuseau horaire
        'CONN_MAX_AGE': 0,  # Permet d'éviter les connexions persistantes
        'CONN_HEALTH_CHECKS': False,
    }

    return connections[db_name]
