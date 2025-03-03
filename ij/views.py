from django.shortcuts import render, redirect
import pandas as pd
from .form import FichierCSVForm
from .models import Element
def importer_csv(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        fichier_csv = request.FILES['csv_file']
        
        # Lire le fichier CSV avec pandas
        df = pd.read_csv(fichier_csv)
        
        # Récupérer les colonnes disponibles
        colonnes_disponibles = df.columns.tolist()
        
        # Si l'utilisateur a déjà sélectionné les colonnes
        if 'colonnes' in request.POST:
            colonnes_selectionnees = request.POST.getlist('colonnes')  # Récupérer les colonnes cochées
            
            # Vérifier si les colonnes sélectionnées existent dans le fichier CSV
            df_selected = df[colonnes_selectionnees]
            
            # Insérer les données dans MySQL
            for _, row in df_selected.iterrows():
                Element.objects.create(**row.to_dict())

            return render(request, 'home.html', {
                'message': 'Importation réussie dans MySQL !',
                'colonnes_disponibles': colonnes_disponibles,
                'form': FichierCSVForm()
            })

        return render(request, 'home.html', {
            'form': FichierCSVForm(),
            'colonnes_disponibles': colonnes_disponibles
        })

    return render(request, 'home.html', {'form': FichierCSVForm()})






""" pour rediriger vers le repertoire home """
def home(request):
    return render(request, 'home.html')
