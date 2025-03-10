"""
URL configuration for ij project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import include, path
from .views import connect_database, connect_to_external_db, delete_element, delete_ressource, element_list, get_columns, get_ressource_json, get_table_columns, get_tables, home, element, import_data, ressource, critere,ressource_create, ressource_delete, ressource_update, save_element, get_elements_json, import_elements, import_dataRessource, save_ressource

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('element/', element, name="element"),
    path('ressource/', ressource, name="ressource"),
    path('critere/', critere, name="critere"),
    path('auth/', include('authentification.urls')),
    path('ressource/create/', ressource_create, name='ressource_create'),
    path('ressource/update/<int:id>/', ressource_update, name='ressource_update'),
    path('ressource/delete/<int:id>/', ressource_delete, name='ressource_delete'),
    path("connect-db/", connect_database, name="connect_database"),
    path('elements/', element_list, name='element_list'),
    path('elements/json/', get_elements_json, name='get_elements_json'),
    path('elements/save/', save_element, name='save_element'),
    path('elements/delete/', delete_element, name='delete_element'),
    
    path('get_tables/', get_tables, name='get_tables'),
    path('get_table_columns/', get_table_columns, name='get_table_columns'),
    path('import_elements/', import_elements, name='import_elements'),
    path('import_data/', import_data, name='import_data'),
    
    # URL pour établir la connexion à la base de données externe
    path('connect_to_external_db/', connect_to_external_db, name='connect_to_external_db'),

    # URL pour récupérer les tables de la base de données externe
    path('get_tables/', get_tables, name='get_tables'),

    # URL pour récupérer les colonnes d'une table spécifique
    path('get_columns/', get_columns, name='get_columns'),

    # URL pour importer les données dans la base de données Django
    path('ressource/import_data/', import_dataRessource, name='import_dataRessource'),
    
    
    path('ressource/save/', save_ressource, name='save_ressource'),
    path('ressource/delete/', delete_ressource, name='delete_ressource'),
    path('ressource/json/', get_ressource_json, name='get_ressource_json'),
]
