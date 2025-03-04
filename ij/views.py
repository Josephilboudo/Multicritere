from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
    ressources= Ressource.objects.all()
    return render(request, 'ressource.html', {'ressources': ressources})

def element(request):
    elements = Element.objects.all()
    return render(request, 'element.html', {'elements': elements})

def critere(request):
    return render(request, 'critere.html')

""" Elements """
def element_create(request):
    if request.method == 'POST':
        codeElement = request.POST.get('codeElement')
        nom = request.POST.get('nom')

        if not codeElement or not nom:
            return JsonResponse({'success': False, 'errors': 'Tous les champs sont requis.'})

        element = Element.objects.create(codeElement=codeElement, nom=nom)
        return JsonResponse({'success': True, 'id': element.id, 'codeElement': element.codeElement, 'nom': element.nom})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

def element_update(request, id):
    element = get_object_or_404(Element, id=id)
    if request.method == 'POST':
        element.codeElement = request.POST.get('codeElement')
        element.nom = request.POST.get('nom')
        element.save()
        return JsonResponse({'success': True, 'id': element.id, 'codeElement': element.codeElement, 'nom': element.nom})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

def element_delete(request, id):
    element = get_object_or_404(Element, id=id)
    if request.method == 'POST':
        element.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

""" Ressources """
def ressource_create(request):
    if request.method == 'POST':
        codeRessource = request.POST.get('codeRessource')
        nom = request.POST.get('nom')

        if not codeRessource or not nom:
            return JsonResponse({'success': False, 'errors': 'Tous les champs sont requis.'})

        ressource = Ressource.objects.create(codeRessource=codeRessource, nom=nom)
        return JsonResponse({'success': True, 'id': ressource.id, 'codeRessource': ressource.codeRessource, 'nom': ressource.nom})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

def ressource_update(request, id):
    ressource = get_object_or_404(Ressource, id=id)
    if request.method == 'POST':
        ressource.codeRessource = request.POST.get('codeRessource')
        ressource.nom = request.POST.get('nom')
        ressource.save()
        return JsonResponse({'success': True, 'id': ressource.id, 'codeRessource': ressource.codeRessource, 'nom': ressource.nom})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

def ressource_delete(request, id):
    ressource = get_object_or_404(Ressource, id=id)
    if request.method == 'POST':
        ressource.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})