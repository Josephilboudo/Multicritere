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
from django.contrib import admin
from django.urls import include, path
from .views import home, element, ressource, critere, element_create, element_update, element_delete, ressource_create, ressource_delete, ressource_update, import_csv, import_csv_ressource

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('element/', element, name="element"),
    path('ressource/', ressource, name="ressource"),
    path('critere/', critere, name="critere"),
    path('auth/', include('authentification.urls')),
    path('element/create/', element_create, name='element_create'),
    path('element/update/<int:id>/', element_update, name='element_update'),
    path('element/delete/<int:id>/', element_delete, name='element_delete'),
    path("element/import-csv/", import_csv, name="import_csv"),
    path("ressource/import-csv/", import_csv_ressource, name="import_csv_ressource"),
    path('ressource/create/', ressource_create, name='ressource_create'),
    path('ressource/update/<int:id>/', ressource_update, name='ressource_update'),
    path('ressource/delete/<int:id>/', ressource_delete, name='ressource_delete'),
]
