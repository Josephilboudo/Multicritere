import math
import random
from copy import deepcopy

from django.http import JsonResponse

from ij.algorithmeGenetique import evaluer_fitness, evolution_genetique
from ij.calcul import verifier_contraintes_solution
from ij.models import Contrainte, Element, Objectif

def recuit_simule_multiobj(
    solution_initiale, 
    contraintes, 
    max_iterations=1000, 
    temperature_initiale=100.0, 
    taux_refroidissement=0.95
):
    """
    Algorithme de recuit simulé pour optimisation multicritère
    
    Args:
    - solution_initiale: Solution de départ
    - contraintes: Contraintes à respecter
    - max_iterations: Nombre maximal d'itérations
    - temperature_initiale: Température de départ
    - taux_refroidissement: Taux de réduction de la température
    
    Returns:
    - Meilleure solution trouvée
    """
    # Solution courante
    solution_courante = deepcopy(solution_initiale)
    
    # Meilleure solution
    meilleure_solution = deepcopy(solution_courante)
    
    # Température
    temperature = temperature_initiale
    
    # Historique des améliorations
    historique_ameliorations = []
    
    def calculer_score_total(objectifs):
        """
        Calcule un score agrégé pour comparer les solutions
        """
        return sum(objectifs.values())
    
    def generer_voisin(solution):
        """
        Génère une solution voisine par mutation
        """
        # Copie de la solution
        voisin = deepcopy(solution)
        
        # Récupérer tous les éléments
        elements = list(Element.objects.all())
        
        # Choisir un nombre aléatoire d'éléments à modifier
        nb_mutations = max(1, int(len(voisin['data']) * 0.2))
        indices_mutation = random.sample(range(len(voisin['data'])), nb_mutations)
        
        for idx in indices_mutation:
            # Filtrer les candidats
            candidats = [
                elem for elem in elements 
                if elem.codeElement.startswith(voisin['data'][idx]['couplage'].split('_')[0])
            ]
            
            if candidats:
                nouvel_element = random.choice(candidats)
                voisin['data'][idx]['couplage'] = nouvel_element.codeElement
        
        # Vérifier les contraintes
        if verifier_contraintes_solution(voisin['data'], contraintes):
            # Recalculer les objectifs
            voisin['objectifs'] = evaluer_fitness(
                voisin['data'], 
                Objectif.objects.all()
            )
            return voisin
        
        return solution
    
    def probabilite_acceptation(delta_score, temperature):
        """
        Calcule la probabilité d'accepter une solution moins bonne
        """
        if delta_score < 0:
            return 1.0
        return math.exp(-delta_score / temperature)
    
    # Boucle principale du recuit simulé
    for iteration in range(max_iterations):
        # Générer un voisin
        voisin = generer_voisin(solution_courante)
        
        # Calculer les scores
        score_courant = calculer_score_total(solution_courante['objectifs'])
        score_voisin = calculer_score_total(voisin['objectifs'])
        
        # Différence de score
        delta_score = score_voisin - score_courant
        
        # Critère d'acceptation
        if delta_score < 0 or random.random() < probabilite_acceptation(delta_score, temperature):
            solution_courante = voisin
            
            # Mise à jour de la meilleure solution
            if calculer_score_total(solution_courante['objectifs']) < calculer_score_total(meilleure_solution['objectifs']):
                meilleure_solution = deepcopy(solution_courante)
                historique_ameliorations.append({
                    'iteration': iteration,
                    'score': calculer_score_total(meilleure_solution['objectifs']),
                    'objectifs': meilleure_solution['objectifs']
                })
        
        # Réduction de la température
        temperature *= taux_refroidissement
        
        # Critère d'arrêt optionnel
        if temperature < 0.01:
            break
    
    # Affichage des améliorations
    print("Historique des améliorations:")
    for amelioration in historique_ameliorations:
        print(f"Itération {amelioration['iteration']}: Score {amelioration['score']}, Objectifs {amelioration['objectifs']}")
    
    return meilleure_solution

def hybride_genetique_recuit(
    taille_population, 
    contraintes, 
    generations_genetique=20,
    iterations_recuit=1000
):
    """
    Algorithme hybride combinant génétique et recuit simulé
    Garantit un retour de population de la taille demandée
    """
    # Étape 1 : Algorithme génétique
    population_genetique = evolution_genetique(
        taille_population, 
        contraintes, 
        generations=generations_genetique
    )
    
    # S'assurer que la population a bien la taille demandée
    if len(population_genetique) < taille_population:
        print(f"Attention : Population génétique plus petite que prévu ({len(population_genetique)})")
    
    # Appliquer le recuit simulé à chaque solution
    population_optimisee = []
    for solution in population_genetique:
        try:
            solution_recuite = recuit_simule_multiobj(
                solution, 
                contraintes, 
                max_iterations=iterations_recuit
            )
            population_optimisee.append(solution_recuite)
        except Exception as e:
            print(f"Erreur lors du recuit simulé : {e}")
            # Conserver la solution originale en cas d'erreur
            population_optimisee.append(solution)
    
    # Compléter la population si nécessaire
    while len(population_optimisee) < taille_population:
        # Dupliquer des solutions existantes si besoin
        population_optimisee.append(random.choice(population_optimisee))
    
    # Tronquer si trop de solutions
    population_optimisee = population_optimisee[:taille_population]
    
    return population_optimisee

# Dans votre vue Django
def generate_population_view(request):
    taille_population = 10
    contraintes = Contrainte.objects.filter(estAppliqueSolution=True).all()
    
    if request.method == 'POST':
        try:
            population = hybride_genetique_recuit(
                taille_population, 
                contraintes, 
                generations_genetique=20, 
                iterations_recuit=10
            )
            
            # Sérialisation sécurisée
            population_serializable = []
            for sol in population:
                try:
                    solution_dict = {
                        'data': sol['data'],
                        'objectifs': {k: float(v) for k, v in sol['objectifs'].items()}
                    }
                    population_serializable.append(solution_dict)
                except Exception as e:
                    print(f"Erreur de sérialisation : {e}")
            
            print(f"taille: {len(population)}")
            if population:
                print(f"pop1 {population[0]}")
                if len(population) > 1:
                    print(f"pop2 {population[1]}")
            
            return JsonResponse({
                'message': 'Population générée avec succès!', 
                'population': population_serializable
            })
        
        except Exception as e:
            print(f"Erreur lors de la génération de population : {e}")
            return JsonResponse({
                'error': str(e)
            }, status=500)
# Utilisation
# resultat_final = hybride_genetique_recuit(
#     taille_population=100, 
#     contraintes=vos_contraintes
# )