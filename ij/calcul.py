import datetime
import json
from django.db import connections
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ij.models import Contrainte, Couplage, CouplageCritere, Critere, Element, Ressource


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



#verification des contraintes existantes

def filtrer_couplage_criteres():
    try:
        contraintes = Contrainte.objects.all()
        couplages = CouplageCritere.objects.all()
        # Liste des IDs à supprimer
        ids_a_supprimer = []
        for couplage in couplages:
            valeurs = couplage.valeur  # Récupèrer le champ JSON comme dictionnaire
            # Vérifier si c'est une chaîne JSON et la convertir en dict
            if isinstance(valeurs, str):
                try:
                    valeurs = json.loads(valeurs.replace("'", "\""))  # Convertir en dict (corriger les guillemets si besoin)
                except json.JSONDecodeError:
                    continue

            for contrainte in contraintes:
                critere_cible = contrainte.critere_cible
                seuil = contrainte.seuil
                type_contrainte = contrainte.type
                valeur_critere_cible = valeurs[critere_cible]  # Valeur à tester

                if seuil in valeurs:
                    seuil = valeurs[seuil]

                # Appliquer la contrainte
                if not respecter_contrainte(valeur_critere_cible, seuil, type_contrainte):
                    ids_a_supprimer.append(couplage.idValeur)
                    break

        # Supprimer les éléments qui ne respectent pas les contraintes
        CouplageCritere.objects.filter(idValeur__in=ids_a_supprimer).delete()

        return {"status": "success", "message": f"{len(ids_a_supprimer)} éléments supprimés"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
#Fonction pour la verification du respect des contraintes
def respecter_contrainte(valeur, seuil, type_contrainte):

    try:
        # Vérifier si c'est une date (format YYYY-MM-DD)
        if isinstance(valeur, str) and isinstance(seuil, str):
            try:
                valeur = datetime.strptime(valeur, "%Y-%m-%d")
                seuil = datetime.strptime(seuil, "%Y-%m-%d")
            except ValueError:
                pass  # Si ce n'est pas une date, on continue avec les nombres

        # Conversion en float si possible
        try:
            valeur = float(valeur)
            seuil = float(seuil)
        except ValueError:
            pass  # Laisser la valeur telle quelle si ce n'est pas un nombre


        if type_contrainte == '>':
            return valeur > seuil
        elif type_contrainte == '<':
            return valeur < seuil
        elif type_contrainte == '=':
            return valeur == seuil
        elif type_contrainte == '>=':
            return valeur >= seuil
        elif type_contrainte == '<=':
            return valeur <= seuil
        else:
            return False  # Type inconnu, la contrainte n'est pas respectée
    except ValueError:
        return False  # Si conversion impossible, contrainte non respectée

@csrf_exempt  # Désactive la vérification CSRF pour les tests (à sécuriser ensuite)
def verifier_contraintes(request):
    if request.method == "POST":
        result = filtrer_couplage_criteres()  # Appel de la fonction
        return JsonResponse(result)  # Retourne le résultat au frontend
    return JsonResponse({"status": "error", "message": "Requête invalide"}, status=400)




