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
from .views import connect_database, delete_element, element_list, home, element, ressource, critere,ressource_create, ressource_delete, ressource_update, import_csv, import_csv_ressource, save_element, get_elements_json, get_table_data, import_elements

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('element/', element, name="element"),
    path('ressource/', ressource, name="ressource"),
    path('critere/', critere, name="critere"),
    path('auth/', include('authentification.urls')),

    path("element/import-csv/", import_csv, name="import_csv"),
    path("ressource/import-csv/", import_csv_ressource, name="import_csv_ressource"),
    path('ressource/create/', ressource_create, name='ressource_create'),
    path('ressource/update/<int:id>/', ressource_update, name='ressource_update'),
    path('ressource/delete/<int:id>/', ressource_delete, name='ressource_delete'),
    path("connect-db/", connect_database, name="connect_database"),
    path('elements/', element_list, name='element_list'),
    path('elements/json/', get_elements_json, name='get_elements_json'),
    path('elements/save/', save_element, name='save_element'),
    path('elements/delete/', delete_element, name='delete_element'),
    path('get_table_data/', get_table_data, name='get_table_data'),
    path('import_elements/', import_elements, name='import_elements'),
]
