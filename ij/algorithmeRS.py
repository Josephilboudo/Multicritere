import json
import random
import math

def fonction_objectif(solution):
    """
    Évalue une solution en fonction des objectifs (compétence, charge de travail, etc.).
    
    :param solution: Dictionnaire contenant "data" et "objectifs"
    :return: Score global de la solution
    """
    score = 0
    
    # Extraction des objectifs
    objectifs = solution.get("objectifs", {})
    
    # Parcours des données de la solution
    for element in solution.get("data", []):
        if isinstance(element, dict) and "valeur" in element:
            # Convertir la chaîne JSON en dictionnaire
            valeurs = json.loads(element["valeur"])
            
            # Ajouter les valeurs des critères aux objectifs
            for critere, valeur in valeurs.items():
                if critere in objectifs:
                    score += objectifs[critere] * valeur  # On applique l'objectif correspondant

    return score


def generer_voisin(solution):
    """
    Génère une solution voisine en modifiant légèrement une des valeurs de 'data'.
    """
    voisin = solution.copy()
    if "data" in voisin and len(voisin["data"]) > 1:
        index = random.randint(0, len(voisin["data"]) - 1)  # Choisir un élément au hasard
        if isinstance(voisin["data"][index], str):  # Changer un élément aléatoire
            voisin["data"][index] = random.choice(["c1", "c2", "c3", "c4", "c5", "c6"])  # Choix arbitraire
    return voisin

def recuit_simule(solution_initiale, temperature_initiale=1000, alpha=0.95, Tmin=1):
    """
    Algorithme du Recuit Simulé pour améliorer la solution.
    
    :param solution_initiale: Solution de départ (issue de l'algorithme génétique)
    :param temperature_initiale: Température de départ
    :param alpha: Facteur de refroidissement (0 < alpha < 1)
    :param Tmin: Température minimale
    :return: Meilleure solution trouvée
    """
    # Initialisation
    solution_actuelle = solution_initiale
    meilleure_solution = solution_initiale
    meilleure_valeur = fonction_objectif(solution_initiale)
    
    T = temperature_initiale  # Température actuelle
    
    while T > Tmin:
        # Générer un voisin
        voisin = generer_voisin(solution_actuelle)
        valeur_voisin = fonction_objectif(voisin)
        
        # Calcul de la variation de score
        delta = valeur_voisin - meilleure_valeur
        
        # Décision d'acceptation
        if delta > 0 or random.uniform(0, 1) < math.exp(delta / T):
            solution_actuelle = voisin
            if valeur_voisin > meilleure_valeur:
                meilleure_solution = voisin
                meilleure_valeur = valeur_voisin
        
        # Refroidissement
        T *= alpha
    
    return meilleure_solution
