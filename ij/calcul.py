from collections import defaultdict
from datetime import datetime
from decimal import Decimal
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
                    
                if result and result[0] is not None:
                    try:
                        # Si c'est un Decimal
                        valeurs_criteres[critere.nom] = float(result[0])
                    except (TypeError, ValueError):
                        try:
                            # Si c'est un datetime
                            valeurs_criteres[critere.nom] = result[0].isoformat()
                        except (AttributeError, TypeError):
                        # Autre type
                            valeurs_criteres[critere.nom] = result[0]
                else:
                    valeurs_criteres[critere.nom] = None

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
        contraintes = Contrainte.objects.filter(estAppliqueSolution=False)
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

from datetime import datetime

def respecter_contrainte(valeur, seuil, type_contrainte):
    try:
        # Vérifier si c'est une date (format YYYY-MM-DD)
        if isinstance(valeur, str) and isinstance(seuil, str):
            try:
                valeur = datetime.strptime(valeur, "%Y-%m-%d")
                seuil = datetime.strptime(seuil, "%Y-%m-%d")
                
                # Si ce sont des dates, comparer directement sans conversion en float
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
                    return False
            except ValueError:
                # Ce n'est pas une date, on continue avec les nombres
                pass

        # Conversion en float pour les nombres
        try:
            # Assurez-vous de ne pas essayer de convertir un datetime en float
            if not isinstance(valeur, datetime) and not isinstance(seuil, datetime):
                valeur = float(valeur)
                seuil = float(seuil)
        except (ValueError, TypeError):
            pass  # Laisser la valeur telle quelle si ce n'est pas un nombre

        # Comparaison finale
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
    except Exception as e:
        print(f"Erreur dans respecter_contrainte: {e}")
        return False  # Si une erreur se produit, contrainte non respectée

#vue pour la fonction de verification de contraintes sur les solutions
@csrf_exempt  # Désactive la vérification CSRF pour les tests (à sécuriser ensuite)
def verifier_contraintes(request):
    if request.method == "POST":
        result = filtrer_couplage_criteres()  # Appel de la fonction
        return JsonResponse(result)  # Retourne le résultat au frontend
    return JsonResponse({"status": "error", "message": "Requête invalide"}, status=400)



import json
from collections import defaultdict

def verifier_contraintes_solution(solution, contraintes):
    # Dictionnaire pour regrouper les valeurs des critères par ressource
    aggregation_criteres = defaultdict(lambda: defaultdict(float))

    # Étape 1: Groupement des valeurs par ressource
    for item in solution:
        print(f"Traitement de l'élément: {item}")  # Debugging: Vérifier l'élément de solution
        if isinstance(item, dict) and 'couplage' in item:
            # L'item est un dictionnaire, donc c'est un CouplageCritere sérialisé
            couplage_id = item['couplage']
            valeur_criteres = item['valeur']
            
            # Vérification si 'valeur' est un dictionnaire
            if isinstance(valeur_criteres, str):
                print(f"Valeur sérialisée trouvée, tentative de conversion en dictionnaire: {valeur_criteres}")  # Debugging
                try:
                    valeur_criteres = json.loads(valeur_criteres)  # Convertir la valeur sérialisée en dictionnaire
                except json.JSONDecodeError:
                    print(f"Erreur de conversion JSON pour {valeur_criteres}")  # Debugging
                    continue  # Si la conversion échoue, ignorer cet élément
            elif not isinstance(valeur_criteres, dict):
                continue  # Passer à l'élément suivant si 'valeur' n'est pas un dictionnaire

        # Vérification que l'objet Couplage existe bien dans la base de données
        try:
            couplage = Couplage.objects.get(id=couplage_id)  # Récupérer l'objet Couplage
            ressource = couplage.ressource  # Accéder à la ressource
        except Couplage.DoesNotExist:
            print(f"Couplage avec ID {couplage_id} introuvable")  # Debugging
            continue  # Si le couplage n'existe pas, passer à l'élément suivant

        # Agrégation des critères
        if isinstance(valeur_criteres, dict):
            for critere, valeur in valeur_criteres.items():
                print(f"Agrégation du critère: {critere} avec valeur {valeur}")  # Debugging
                
                # Vérification si la valeur est None et remplacer par 0
                if valeur is None:
                    print(f"Valeur pour le critère '{critere}' est None, elle sera remplacée par 0.")  # Debugging
                    valeur = 0  # Remplacer None par 0 ou ignorer selon ce que tu préfères

                try:
                    # Si la valeur est une chaîne, la convertir en float
                    if isinstance(valeur, str):
                        valeur = float(valeur)
                except ValueError:
                    print(f"Erreur de conversion de la valeur '{valeur}' pour le critère '{critere}'")  # Debugging
                    continue  # Si la conversion échoue, ignorer cet élément

                aggregation_criteres[ressource][critere] += valeur  # Somme des valeurs par critère

    # Affichage des résultats d'agrégation pour vérification
    print(f"\nAgrégation des critères par ressource : {dict(aggregation_criteres)}")
    for ressource, criteres in aggregation_criteres.items():
        print(f"Ressource: {ressource}, Critères: {criteres}")
        
    if isinstance(contraintes, int):
        # Si contraintes est un ID, récupérer les contraintes associées
        contraintes = Contrainte.objects.filter(estAppliqueSolution=True) 
        if not contraintes.exists():
            return True  # Ou False selon votre logique
    

    # Vérification des contraintes
    for contrainte in contraintes:
        critere_cible = contrainte.critere_cible
        seuil = contrainte.seuil
        type_contrainte = contrainte.type

        print(f"\nVérification de la contrainte : {critere_cible} {type_contrainte} {seuil}")

        for ressource, criteres in aggregation_criteres.items():
            if critere_cible not in criteres:
                print(f"  Pas de critère {critere_cible} trouvé pour la ressource {ressource}")
                continue  # Passer à la ressource suivante si critère non trouvé

            valeur_totale = criteres[critere_cible]
            print(f"  Valeur totale pour {critere_cible} : {valeur_totale}")

            try:
                seuil_numerique = float(seuil)
            except ValueError:
                if seuil in criteres:
                    seuil_numerique = float(criteres[seuil])
                else:
                    print(f"  Seuil {seuil} non trouvé dans les critères pour la ressource {ressource}")
                    continue

            print(f"  Ressource: {ressource} → {critere_cible} = {valeur_totale} (Seuil: {seuil_numerique})")


            # Vérification de la contrainte
            if type_contrainte == "<" and valeur_totale > seuil_numerique:
                print(f"  Contrainte violée : {valeur_totale} > {seuil_numerique}")
                return False  # Contrainte violée
            elif type_contrainte == ">" and valeur_totale < seuil_numerique:
                print(f"  Contrainte violée : {valeur_totale} < {seuil_numerique}")
                return False  # Contrainte violée
            elif type_contrainte == "=" and valeur_totale != seuil_numerique:
                print(f"  Contrainte violée : {valeur_totale} != {seuil_numerique}")
                return False  # Contrainte violée

    return True  # Toutes les contraintes sont respectées
