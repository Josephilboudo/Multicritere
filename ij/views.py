import datetime
from django.conf import settings
from django.db import IntegrityError, connections
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
import json
import csv
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import pandas as pd
from .form import FichierCSVForm
from .models import Element, Ressource, Critere, Contrainte, Solution
from .utils import get_dynamic_connection

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
def element_list(request):
    elements = Element.objects.all().order_by('codeElement')
    return render(request, 'element.html', {'elements': elements})

def get_elements_json(request):
    try:
        elements = Element.objects.all().order_by('codeElement')
        elements_list = []
        
        for element in elements:
            elements_list.append({
                'codeElement': element.codeElement,
                'description': element.description
            })
        
        return JsonResponse({
            'success': True,
            'elements': elements_list
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def save_element(request):
    if request.method == 'POST':
        code = request.POST.get('codeElement')
        desc = request.POST.get('description')
        action = request.POST.get('action')
        
        try:
            if action == 'add':
                # Création d'un nouvel élément
                element = Element(codeElement=code, description=desc)
                element.save()
                return JsonResponse({
                    'success': True,
                    'message': "Élément ajouté avec succès!"
                })
            elif action == 'edit':
                # Modification d'un élément existant
                element = get_object_or_404(Element, codeElement=code)
                element.description = desc
                element.save()
                return JsonResponse({
                    'success': True,
                    'message': "Élément modifié avec succès!"
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f"Erreur: {str(e)}"
            })
    
    return JsonResponse({
        'success': False,
        'message': "Méthode non autorisée"
    })

def delete_element(request):
    if request.method == 'POST':
        code = request.POST.get('codeElement')
        try:
            element = get_object_or_404(Element, codeElement=code)
            element.delete()
            return JsonResponse({
                'success': True,
                'message': "Élément supprimé avec succès!"
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f"Erreur: {str(e)}"
            })
    
    return JsonResponse({
        'success': False,
        'message': "Méthode non autorisée"
    })
    """ Ressources """
def ressource_create(request):
    if request.method == 'POST':
        codeRessource = request.POST.get('codeRessource')
        description = request.POST.get('description')

        if not codeRessource or not description:
            return JsonResponse({'success': False, 'errors': 'Tous les champs sont requis.'})

        ressource = Ressource.objects.create(codeRessource=codeRessource, description=description)
        return JsonResponse({'success': True, 'id': ressource.id, 'codeRessource': ressource.codeRessource, 'description': ressource.description})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

def ressource_update(request, id):
    ressource = get_object_or_404(Ressource, id=id)
    if request.method == 'POST':
        ressource.codeRessource = request.POST.get('codeRessource')
        ressource.description = request.POST.get('description')
        ressource.save()
        return JsonResponse({'success': True, 'id': ressource.id, 'codeRessource': ressource.codeRessource, 'description': ressource.description})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})

def ressource_delete(request, id):
    ressource = get_object_or_404(Ressource, id=id)
    if request.method == 'POST':
        ressource.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': 'Requête invalide.'})


@csrf_exempt
def import_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        selected_columns = json.loads(request.POST.get("columns", "[]"))

        if not selected_columns:
            return JsonResponse({"error": "Aucune colonne sélectionnée"}, status=400)

        # Sauvegarder temporairement le fichier
        file_path = default_storage.save(f"temp/{csv_file.name}", csv_file)

        # Lire le fichier CSV
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            imported_count = 0

            for row in reader:
                # Vérifier que les colonnes existent dans le fichier
                if all(col in row for col in selected_columns):
                    code = row.get("codeElement", "").strip()
                    nom = row.get("nom", "").strip()

                    if code and nom:  # Éviter d'insérer des données vides
                        Element.objects.update_or_create(
                            codeElement=code,
                            defaults={"nom": nom}
                        )
                        imported_count += 1

        return JsonResponse({"message": f"{imported_count} éléments importés avec succès !"})

    return JsonResponse({"error": "Requête invalide"}, status=400)

@csrf_exempt
def import_csv_ressource(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        selected_columns = json.loads(request.POST.get("columns", "[]"))

        if not selected_columns:
            return JsonResponse({"error": "Aucune colonne sélectionnée"}, status=400)

        # Sauvegarder temporairement le fichier
        file_path = default_storage.save(f"temp/{csv_file.name}", csv_file)

        # Lire le fichier CSV
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            imported_count = 0

            for row in reader:
                # Vérifier que les colonnes existent dans le fichier
                if all(col in row for col in selected_columns):
                    code = row.get("codeRessource", "").strip()
                    nom = row.get("nom", "").strip()

                    if code and nom:  # Éviter d'insérer des données vides
                        Ressource.objects.update_or_create(
                            codeRessource=code,
                            defaults={"nom": nom}
                        )
                        imported_count += 1

        return JsonResponse({"message": f"{imported_count} éléments importés avec succès !"})

    return JsonResponse({"error": "Requête invalide"}, status=400)

def connect_database(request):
    if request.method == "POST":
        db_name = request.POST.get("database_name")
        name = request.POST.get("user")
        password = request.POST.get("password")

        try:
            connection = get_dynamic_connection(db_name, name, password)

            with connection.cursor() as cursor:
                cursor.execute("SELECT DATABASE();")  # Vérifie la connexion
                active_db = cursor.fetchone()
                print("Base de données active :", active_db)

                cursor.execute("SHOW TABLES;")
                tables = [row[0] for row in cursor.fetchall()]
                print("Tables trouvées :", tables)

                first_table = tables[0] if tables else None
                data = []
                columns = []

                if first_table:
                    cursor.execute(f"SELECT * FROM {first_table} LIMIT 10;")  # Limite à 10 lignes
                    columns = [col[0] for col in cursor.description]  # Récupérer les noms des colonnes
                    data = cursor.fetchall()
                    print("Colonnes :", columns)
                    print("Données :", data)

            # Retourne un JSON pour AJAX
            return JsonResponse({
                "status": "success",
                "message": f"Connexion réussie à {db_name}",
                "tables": tables,
                "columns": columns,
                "data": data
            })

        except Exception as e:
            print("Erreur de connexion :", e)
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Requête invalide"}, status=400)

def get_table_data(request):
    """
    Récupère les données d'une table spécifique.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            db_name = data.get("dbName")
            table_name = data.get("tableName")
            
            # Vérifier que la base de données est déjà configurée
            if db_name not in settings.DATABASES:
                return JsonResponse({
                    "status": "error", 
                    "message": "Base de données non connectée"
                })
            
            # Obtenir la connexion
            connection = connections[db_name]
            
            with connection.cursor() as cursor:
                # Extraire les données de la table
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 50;")
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
                # Convertir les données en format JSON-sérialisable
                serializable_rows = []
                for row in rows:
                    serializable_row = []
                    for item in row:
                        if isinstance(item, (datetime.date, datetime.datetime)):
                            serializable_row.append(item.isoformat())
                        else:
                            serializable_row.append(item)
                    serializable_rows.append(serializable_row)
                
                return JsonResponse({
                    "status": "success",
                    "columns": columns,
                    "data": serializable_rows
                })
                
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
    
    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée"
    }, status=405)

def import_elements(request):
    """
    Importe des éléments depuis une autre base de données.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            elements = data.get("elements", [])
            
            # Compter les éléments importés et les éléments en erreur
            imported_count = 0
            error_count = 0
            
            # Utiliser le modèle Element pour créer ou mettre à jour les éléments
            for element_data in elements:
                try:
                    # On suppose que vous avez un modèle Element avec les champs codeElement et description
                    # Utiliser get_or_create pour éviter les doublons
                    element, created = Element.objects.get_or_create(
                        codeElement=element_data['codeElement'],
                        defaults={'description': element_data['description']}
                    )
                    
                    if not created:
                        # Mettre à jour la description si l'élément existe déjà
                        element.description = element_data['description']
                        element.save()
                    
                    imported_count += 1
                except Exception as element_error:
                    print(f"Erreur lors de l'importation de l'élément {element_data.get('codeElement')}: {element_error}")
                    error_count += 1
            
            message = f"{imported_count} élément(s) importé(s) avec succès."
            if error_count > 0:
                message += f" {error_count} élément(s) n'ont pas pu être importés."
            
            return JsonResponse({
                "success": True,
                "message": message
            })
            
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Erreur lors de l'importation: {str(e)}"
            })
    
    return JsonResponse({
        "success": False,
        "message": "Méthode non autorisée"
    }, status=405)