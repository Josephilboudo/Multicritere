from django.shortcuts import render
import pandas as pd
from .form import FichierCSVForm
from .models import Element, Ressource, Critere, Contrainte, Solution

def home(request):
    message = None
    colonnes_disponibles = []
    total_elements = Element.objects.count()
    total_ressources = Ressource.objects.count()
    total_criteres = Critere.objects.count()
    total_contraintes = Contrainte.objects.count()
    
    solutions = Solution.objects.all()
    
    if request.method == 'POST' and 'csv_file' in request.FILES:
        fichier_csv = request.FILES['csv_file']
        df = pd.read_csv(fichier_csv)
        colonnes_disponibles = df.columns.tolist()
        print("request.POST:", request.POST) 
        
        if 'colonnes' in request.POST:
            colonnes_selectionnees = request.POST.getlist('colonnes')
            df_selected = df[colonnes_selectionnees]
            print(f"Colonnes sélectionnées : {colonnes_selectionnees}") 
            
            for _, row in df_selected.iterrows():
                Element.objects.create(**row.to_dict())
                print("insertion")
            
            message = 'Importation réussie dans MySQL !'
    
    return render(request, 'home.html', {
        'form': FichierCSVForm(),
        'colonnes_disponibles': colonnes_disponibles,
        'message': message,
        'total_elements': total_elements,
        'total_ressources': total_ressources,
        'total_criteres': total_criteres,
        'total_contraintes': total_contraintes,
        'solutions': solutions,
        
    })
def ressource(request):
    return render(request, 'ressource.html')

def element(request):
    return render(request, 'element.html')

def critere(request):
    return render(request, 'critere.html')
