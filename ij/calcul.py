import json
from django.db import connections
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ij.models import Couplage, CouplageCritere, Critere, Element, Ressource


def calculer_cout():
    # Récupérer tous les couplages existants
    couplages = Couplage.objects.all()
    print("appeler")
    # Récupérer tous les critères
    criteres = Critere.objects.all()
    
    for couplage in couplages:
        # Initialiser un dictionnaire pour stocker les valeurs des critères
        valeurs_criteres = {}

        for critere in criteres:
            # Récupérer l'expression SQL associée au critère
            expression_sql = critere.expression

            # Remplacer les paramètres codeElement et codeRessource dans la requête SQL
            sql_query = expression_sql.replace("x1", f"'{couplage.element_id}'").replace("y1", f"'{couplage.ressource_id}'")
            print(sql_query)
            try:
                # Connexion à la base de données externe et exécution de la requête
                with connections['external_db'].cursor() as cursor:
                    cursor.execute(sql_query)
                    result = cursor.fetchone()  # Supposons qu'on récupère un seul résultat
                    print(result)
                # Stocker la valeur du critère
                if result:
                    valeurs_criteres[critere.nom] = result[0]  # Prendre la première colonne retournée
                else:
                    valeurs_criteres[critere.nom] = None  # Si aucun résultat, mettre None

            except Exception as e:
                print(f"Erreur lors de l'exécution de la requête SQL pour {critere.nom} : {e}")
                valeurs_criteres[critere.nom] = None  # Gérer l'erreur

        # Stocker les valeurs calculées dans CouplageCritere
        CouplageCritere.objects.update_or_create(
            couplage=couplage,
            defaults={"valeur": json.dumps(valeurs_criteres)}
        )

    print("Calcul des coûts terminé avec succès !")
    
    #calculer cout critere
    
@csrf_exempt  # Permet de désactiver la vérification CSRF pour cette vue (à utiliser avec précaution)
def calculer_cout_view(request):
    if request.method == 'POST':
        try:
            calculer_cout()  # Appeler la fonction de calcul des coûts
            return JsonResponse({"status": "success", "message": "Calcul des coûts terminé avec succès !"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)
    
def generer_couplages():
    # Récupérer tous les éléments et toutes les ressources
    elements = Element.objects.all()
    ressources = Ressource.objects.all()

    couplages_crees = 0  # Compteur pour suivre le nombre de couplages créés

    for element in elements:
        for ressource in ressources:
            # Générer l'ID du couplage
            id_couplage = f"{element.codeElement}_{ressource.codeRessource}"

            # Vérifier si le couplage existe déjà pour éviter les doublons
            couplage, created = Couplage.objects.get_or_create(
                id=id_couplage,
                defaults={"element": element, "ressource": ressource}
            )

            if created:
                couplages_crees += 1  # Incrémenter le compteur si un nouveau couplage est créé

    print(f"{couplages_crees} couplage(s) créé(s) avec succès !")

@csrf_exempt  # Permet de désactiver la vérification CSRF pour cette vue (à utiliser avec précaution)
def generer_couplages_view(request):
    if request.method == 'POST':
        try:
            generer_couplages()  # Appeler la fonction de génération des couplages
            return JsonResponse({"status": "success", "message": "Génération des couplages terminée avec succès !"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)
