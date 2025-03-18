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
from .models import CouplageCritere, Element, Ressource, Critere, Contrainte, Solution, Couplage, Objectif
from .utils import get_dynamic_connection

def home(request):
    total_elements = Element.objects.count()
    total_ressources = Ressource.objects.count()
    total_criteres = Critere.objects.count()
    total_contraintes = Contrainte.objects.count()
    
    solutions = Solution.objects.all()
    
    return render(request, 'home.html', {
        'total_elements': total_elements,
        'total_ressources': total_ressources,
        'total_criteres': total_criteres,
        'total_contraintes': total_contraintes,
        'solutions': solutions,
        
    })
def ressource(request):
    ressources= Ressource.objects.all().order_by('codeRessource')
    return render(request, 'ressource.html', {'ressources': ressources})

def crit(request):
    return render(request, 'crit.html')

def element(request):
    elements = Element.objects.all().order_by('codeElement')
    return render(request, 'element.html', {'elements': elements})

def critere(request):
    criteres = Critere.objects.all()
    return render(request, 'critere.html', {'criteres':criteres})

def couplage(request):
    couplages = Couplage.objects.all()
    elements = Element.objects.all()
    ressources = Ressource.objects.all()
     # Fusionner tous les dictionnaires en un seul
    context = {
        'couplages': couplages,
        'elements': elements,
        'ressources': ressources,
    }
    return render(request, 'couplage.html', context)

def objectif(request):
    objectifs = Objectif.objects.all()
    criteres = Critere.objects.all()
    return render(request, 'objectif.html', {'objectifs':objectifs, 'criteres': criteres})


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

def connect_database(request):
    if request.method == "POST":
        db_name = request.POST.get("database_name")
        name = request.POST.get("user")
        password = request.POST.get("password")

        try:
            connection = get_dynamic_connection(db_name, name, password)
            
            request.session['db_credentials'] = {
                'db_name': db_name,
                'name': name,
                'password': password
            }
            request.session.save()
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
                "data": data,
            })

        except Exception as e:
            print("Erreur de connexion :", e)
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Requête invalide"}, status=400)
  
 # importe des donnees duipuis ne bd et les mets dans element 
def import_elements(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            elements = data.get("elements", [])
            
            imported_count = 0
            error_count = 0
            
            for element_data in elements:
                try:
                    # Créer ou mettre à jour l'élément
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

#Récupère la liste des tables de la base de données connectée.
  
    
#test
def get_table_columns(request):
    print("Vue get_table_columns appelée")  # Log de débogage
    if request.method == "POST":
        try:
            # Récupérer le nom de la table depuis le corps de la requête
            data = json.loads(request.body)
            table_name = data.get("tableName")
            print(f"Nom de la table reçu : {table_name}")  # Log de débogage

            if not table_name:
                return JsonResponse({
                    "status": "error", 
                    "message": "Le nom de la table est requis"
                }, status=400)

            # Récupérer les identifiants de la session
            credentials = request.session.get('db_credentials')
            if not credentials:
                return JsonResponse({
                    "status": "error", 
                    "message": "Aucune connexion établie. Veuillez vous connecter d'abord."
                }, status=401)

            db_name = credentials.get('db_name')
            name = credentials.get('name')
            password = credentials.get('password')

            # Établir la connexion
            connection = get_dynamic_connection(db_name, name, password)

            with connection.cursor() as cursor:
                # Récupérer les colonnes de la table (en utilisant des backticks pour échapper le nom de la table)
                cursor.execute(f"DESCRIBE `{table_name}`;")
                columns = [row[0] for row in cursor.fetchall()]
                print(f"Colonnes récupérées : {columns}")  # Log de débogage

                return JsonResponse({
                    "status": "success",
                    "columns": columns,
                })

        except Exception as e:
            print(f"Erreur dans get_table_columns : {e}")  # Log de débogage
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée"
    }, status=405)

def import_data(request):
    print("Vue import_data appelée")  # Log de débogage
    if request.method == 'POST':
        try:
            # Récupérer les données depuis le corps de la requête
            data = json.loads(request.body)
            table_name = data.get('tableName')
            code_column = data.get('codeColumn')
            description_column = data.get('descriptionColumn')

            print(f"Données reçues : table_name={table_name}, code_column={code_column}, description_column={description_column}")  # Log de débogage

            if not table_name or not code_column or not description_column:
                return JsonResponse({
                    "status": "error", 
                    "message": "Tous les champs sont requis (tableName, codeColumn, descriptionColumn)"
                }, status=400)

            # Connexion à la base de données externe
            with connections['external_db'].cursor() as cursor:
                # Récupérer les données de la table
                cursor.execute(f"SELECT `{code_column}`, `{description_column}` FROM `{table_name}`")
                rows = cursor.fetchall()
                print(f"Lignes récupérées : {rows}")  # Log de débogage

                # Insérer les données dans la base de données locale
                for row in rows:
                    Element.objects.create(
                        codeElement=row[0],
                        description=row[1]
                    )

            return JsonResponse({"status": "success", "message": "Données importées avec succès"})
        except Exception as e:
            print(f"Erreur dans import_data : {e}")  # Log de débogage
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

def get_columns(request):
    print("Vue get_columns appelée")  # Log de débogage
    if request.method == 'POST':
        try:
            # Récupérer le nom de la table depuis le corps de la requête
            data = json.loads(request.body)
            table_name = data.get('tableName')
            print(f"Nom de la table reçu : {table_name}")  # Log de débogage

            if not table_name:
                return JsonResponse({"status": "error", "message": "Le nom de la table est requis"}, status=400)

            # Connexion à la base de données externe
            with connections['external_db'].cursor() as cursor:
                # Récupérer les colonnes de la table (en utilisant des backticks pour échapper le nom de la table)
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = [row[0] for row in cursor.fetchall()]
                print(f"Colonnes récupérées : {columns}")  # Log de débogage

            return JsonResponse({"status": "success", "columns": columns})
        except Exception as e:
            print(f"Erreur dans get_columns : {e}")  # Log de débogage
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

def get_tables(request):
    if request.method == 'GET':
        try:
            # Vérifier si la configuration de la base de données externe est stockée dans la session
            if 'external_db_config' not in request.session:
                return JsonResponse({"status": "error", "message": "Aucune configuration de base de données externe trouvée"}, status=400)

            # Configurer la connexion dynamique
            connections.databases['external_db'] = request.session['external_db_config']

            # Utiliser la connexion
            with connections['external_db'].cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]

            return JsonResponse({"status": "success", "tables": tables})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

def connect_to_external_db(request):
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            data = json.loads(request.body)
            db_name = data.get('dbName')
            db_user = data.get('dbUser')
            db_password = data.get('dbPassword')
            db_host = data.get('dbHost')
            db_port = data.get('dbPort')

            # Stocker les informations de connexion dans la session
            request.session['external_db_config'] = {
                'ENGINE': 'django.db.backends.mysql',  # Ou autre moteur de base de données
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'TIME_ZONE': settings.TIME_ZONE,
                'CONN_MAX_AGE': 0,
                'CONN_HEALTH_CHECKS': False,
                'ATOMIC_REQUESTS': False,
                'AUTOCOMMIT': True,
                'OPTIONS': {
                    'charset': 'utf8mb4',
                },
            }
            connections.databases['external_db'] = request.session['external_db_config']
            # Tester la connexion
            with connections['external_db'].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            return JsonResponse({"status": "success", "message": "Connexion réussie"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)
#ressource
def import_dataRessource(request):
    print("Vue import_data appelée")  # Log de débogage
    if request.method == 'POST':
        try:
            # Récupérer les données depuis le corps de la requête
            data = json.loads(request.body)
            table_name = data.get('tableName')
            code_column = data.get('codeColumn')
            description_column = data.get('descriptionColumn')

            print(f"Données reçues : table_name={table_name}, code_column={code_column}, description_column={description_column}")  # Log de débogage

            if not table_name or not code_column or not description_column:
                return JsonResponse({
                    "status": "error", 
                    "message": "Tous les champs sont requis (tableName, codeColumn, descriptionColumn)"
                }, status=400)

            # Connexion à la base de données externe
            with connections['external_db'].cursor() as cursor:
                # Récupérer les données de la table
                cursor.execute(f"SELECT `{code_column}`, `{description_column}` FROM `{table_name}`")
                rows = cursor.fetchall()
                print(f"Lignes récupérées : {rows}")  # Log de débogage

                # Insérer les données dans la base de données locale
                for row in rows:
                    Ressource.objects.create(
                        codeRessource=row[0],
                        description=row[1]
                    )

            return JsonResponse({"status": "success", "message": "Données importées avec succès"})
        except Exception as e:
            print(f"Erreur dans import_data : {e}")  # Log de débogage
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

def save_ressource(request):
    if request.method == 'POST':
        code = request.POST.get('codeRessource')
        desc = request.POST.get('description')
        action = request.POST.get('action')
        
        try:
            if action == 'add':
                # Création d'un nouvel élément
                ressource = Ressource(codeRessource=code, description=desc)
                ressource.save()
                return JsonResponse({
                    'success': True,
                    'message': "Élément ajouté avec succès!"
                })
            elif action == 'edit':
                # Modification d'un élément existant
                ressource = get_object_or_404(Ressource, codeRessource=code)
                ressource.description = desc
                ressource.save()
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

def delete_ressource(request):
    if request.method == 'POST':
        code = request.POST.get('codeElement')
        try:
            ressource = get_object_or_404(Ressource, codeRessource=code)
            ressource.delete()
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

def get_ressource_json(request):
    try:
        ressources = Ressource.objects.all().order_by('codeRessource')
        ressources_list = []
        
        for ressource in ressources:
            ressources_list.append({
                'codeRessource': ressource.codeRessource,
                'description': ressource.description
            })
            
        print("Données envoyées par Django :", ressources_list)
        
        return JsonResponse({
            'success': True,
            'ressources': ressources_list
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
        
#couplage
def import_dataCouplage(request):
    print("Vue import_dataCouplage appelée")  # Log de débogage
    if request.method == 'POST':
        try:
            # Récupérer les données depuis le corps de la requête
            data = json.loads(request.body)
            table_name = data.get('tableName')
            code_column = data.get('codeColumn')
            description_column = data.get('descriptionColumn')

            print(f"Données reçues : table_name={table_name}, code_column={code_column}, description_column={description_column}")  # Log de débogage

            if not table_name or not code_column or not description_column:
                return JsonResponse({
                    "status": "error", 
                    "message": "Tous les champs sont requis (tableName, codeColumn, descriptionColumn)"
                }, status=400)

            # Connexion à la base de données externe
            with connections['external_db'].cursor() as cursor:
                # Récupérer les données de la table
                cursor.execute(f"SELECT `{code_column}`, `{description_column}` FROM `{table_name}`")
                rows = cursor.fetchall()
                print(f"Lignes récupérées : {rows}")  # Log de débogage

                # Insérer les données dans la base de données locale
                for row in rows:
                    element_id = row[0]
                    ressource_id = row[1]
                    element = Element.objects.get(codeElement=element_id)
                    ressource = Ressource.objects.get(codeRessource=ressource_id)
                    Couplage.objects.create(
                        element=element,
                        ressource=ressource
                    )

            return JsonResponse({"status": "success", "message": "Données importées avec succès"})
        except Exception as e:
            print(f"Erreur dans import_dataCouplage : {e}")  # Log de débogage
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

def save_couplage(request):
    if request.method == 'POST':
        code = request.POST.get('element')
        desc = request.POST.get('ressource')
        action = request.POST.get('action')
        
        try:
            if action == 'add':
                # Création d'un nouvel élément
                element = Element.objects.get(codeElement= code)
                ressource = Ressource.objects.get(codeRessource= desc)
                couplage = Couplage(element=element, ressource=ressource)
                couplage.save()
                return JsonResponse({
                    'success': True,
                    'message': "Couplage ajouté avec succès!"
                })
            elif action == 'edit':
                # Modification d'un élément existant
                couplage_id = request.POST.get('couplageId')
                element_code = request.POST.get('element')
                ressource_code = request.POST.get('ressource')
                couplage = get_object_or_404(Couplage, id=couplage_id)
                # Mettez à jour les relations avec les nouveaux objets
                element = Element.objects.get(codeElement=element_code)
                ressource = Ressource.objects.get(codeRessource=ressource_code)
                couplage.ressource = ressource
                couplage.element = element
                couplage.save()
                return JsonResponse({
                    'success': True,
                    'message': "Couplage modifié avec succès!"
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

def delete_couplage(request):
    if request.method == 'POST':
        code = request.POST.get('element')
        try:
            couplage = get_object_or_404(Couplage, id=code)
            couplage.delete()
            return JsonResponse({
                'success': True,
                'message': "Couplage supprimé avec succès!"
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

def get_couplage_json(request):
    try:
        couplages = Couplage.objects.all().order_by('element')
        couplage_list = []
        
        for couplage in couplages:
            couplage_list.append({
                'id': couplage.id,
                'element': couplage.element.codeElement,
                'ressource': couplage.ressource.codeRessource
            })
            
        print("Données envoyées par Django :", couplage_list)
        
        return JsonResponse({
            'success': True,
            'couplages': couplage_list
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
        



#critere
def get_critere_json(request):
    try:
        criteres = Critere.objects.all().order_by('nom')
        critere_list = []
        
        for critere in criteres:
            critere_list.append({
                'idCritere': critere.idCritere,
                'nom': critere.nom,
                'expression': critere.expression,
                'poids': critere.poids
            })
            
        print("Données envoyées par Django :", critere_list)
        
        return JsonResponse({
            'success': True,
            'criteres': critere_list
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
        
def delete_critere(request):
    if request.method == 'POST':
        critere_id = request.POST.get('idCritere')
        try:
            critere = get_object_or_404(Critere, idCritere=critere_id)
            critere.delete()
            return JsonResponse({
                'success': True,
                'message': "Critère supprimé avec succès!"
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
    
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Critere

@csrf_exempt
def save_critere(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        expression = data.get('expression')

        if not name or not description or not expression:
            return JsonResponse({'success': False, 'error': 'Tous les champs sont obligatoires.'})

        try:
            critere = Critere(nom=name, description=description, expression=expression)
            critere.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})

def execute_join(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            join_type = data.get('joinType')
            table1 = data.get('table1')
            join_column1 = data.get('joinColumn1')
            table2 = data.get('table2')
            join_column2 = data.get('joinColumn2')
            selected_columns = data.get('selectedColumns')

            # Vérifier si une table est virtuelle
            if table1.startswith("Jointure_"):
                # Traiter table1 comme une table virtuelle
                # (Vous devrez stocker les tables virtuelles côté serveur)
                pass
            elif table2.startswith("Jointure_"):
                # Traiter table2 comme une table virtuelle
                pass

            # Générer la requête SQL
            select_clause = selected_columns if selected_columns else "*"
            query = f"""
                SELECT {select_clause} FROM {table1}
                {join_type} {table2}
                ON {table1}.{join_column1} = {table2}.{join_column2}
            """

            # Exécuter la requête
            with connections['external_db'].cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            results = [dict(zip(columns, row)) for row in rows]
            return JsonResponse({"status": "success", "data": results})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)



#objectifs
@csrf_exempt
def add_objectif(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            description = data.get('description')
            type_obj = data.get('type')
            idcritere = data.get('idCouplageCritere')
            
            # Get the Critere object
            try:
                critere = Critere.objects.get(idCritere=idcritere)
                
                # Create and save the Objectif
                objectif = Objectif(description=description, type=type_obj, idCritere=critere)
                objectif.save()
                
                return JsonResponse({'status': 'success', 'id': objectif.idObjectif})
            except Critere.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Critere not found'}, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
@csrf_exempt
def delete_objectif(request, id):
    if request.method == 'DELETE':
        try:
            objectif = Objectif.objects.get(pk=id)
            objectif.delete()
            return JsonResponse({'status': 'success'})
        except Objectif.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Objectif not found'}, status=404)





