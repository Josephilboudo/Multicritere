import random
import math
import copy

def generer_voisin(solution, ensemble_possibilites):
    """Génère un voisin en respectant les contraintes"""
    voisin = copy.deepcopy(solution)
    
    modifiable_indexes = [i for i, item in enumerate(voisin["data"]) if est_modifiable(item)]
    if not modifiable_indexes:
        return solution  

    index = random.choice(modifiable_indexes)
    valeurs_possibles = [val for val in ensemble_possibilites if val != voisin["data"][index]]
    
    if valeurs_possibles:
        voisin["data"][index] = random.choice(valeurs_possibles)

    return voisin

def est_modifiable(element):
    """Détermine si un élément peut être modifié"""
    return not isinstance(element, dict)

def recuit_simule(solution_initiale, ensemble_possibilites, temperature_initiale=100, refroidissement=0.95, iterations=1000, seuil_arret=0.1):
    """Recuit simulé adapté pour multi-objectif multicritère"""
    solution_courante = solution_initiale
    meilleure_solution = solution_courante
    temperature = temperature_initiale

    for _ in range(iterations):
        voisin = generer_voisin(solution_courante, ensemble_possibilites)

        # Évaluation multi-objectif
        score_actuel = fonction_objectif(solution_courante)
        score_voisin = fonction_objectif(voisin)

        # Comparaison multi-objectif
        if est_meilleur(score_voisin, score_actuel) or random.random() < math.exp((sum(score_voisin) - sum(score_actuel)) / temperature):
            solution_courante = voisin
            if est_meilleur(score_voisin, fonction_objectif(meilleure_solution)):
                meilleure_solution = voisin
        
        temperature *= refroidissement
        if temperature < seuil_arret:
            break

    return meilleure_solution

def fonction_objectif(solution):
    """Calcule les scores des différents objectifs sous forme de tuple"""
    scores = {}

    if "objectifs" not in solution:
        return (0, 0)  # Retourne un score nul si aucun objectif n'est défini

    for critere, valeur in solution["objectifs"].items():
        if isinstance(valeur, (int, float)):  
            scores[critere] = valeur

    return tuple(scores.values())  # Retourne un tuple de scores

def est_meilleur(score1, score2):
    """Compare deux solutions en mode multi-objectif (dominance de Pareto)"""
    meilleur_sur_un_critere = False

    for s1, s2 in zip(score1, score2):
        if s1 > s2:  # Une amélioration sur un critère
            meilleur_sur_un_critere = True
        elif s1 < s2:  # Une dégradation sur un critère
            return False

    return meilleur_sur_un_critere  # Retourne True si une amélioration sans régression


def appliquer_recuit_sur_population(population, ensemble_possibilites, temperature_initiale=100, refroidissement=0.95, iterations=1000):
    """Applique le recuit simulé sur chaque individu de la population générée par le GA"""
    population_amelioree = []
    for individu in population:
        solution_amelioree = recuit_simule(individu, ensemble_possibilites, temperature_initiale, refroidissement, iterations)
        population_amelioree.append(solution_amelioree)
    
    return population_amelioree