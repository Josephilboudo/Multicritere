import json
import random

from ij.calcul import verifier_contraintes_solution
from .models import CouplageCritere, Element, Couplage, Objectif
from collections import defaultdict
from datetime import datetime

def generer_population_initiale(taille_population, contraintes):
    # Récupérer tous les éléments (tâches)
    elements = list(Element.objects.all())
    objectifs = Objectif.objects.all()

    # Récupérer tous les couplages critères valides
    couplages_criteres = list(CouplageCritere.objects.select_related('couplage').all())

    # Organiser les couplages critères par élément
    couplages_criteres_par_element = {}
    for cc in couplages_criteres:
        element_id = cc.couplage.element_id  # Récupérer l'élément correspondant
        if element_id not in couplages_criteres_par_element:
            couplages_criteres_par_element[element_id] = []
        couplages_criteres_par_element[element_id].append(cc)

    population = []
    tentatives = 0
    max_tentatives = taille_population * 3  # Pour éviter une boucle infinie

    while len(population) < taille_population and tentatives < max_tentatives:
        tentatives += 1
        solution_data = []

        # Générer une solution en sélectionnant des couplages critères pour chaque élément
        for element in elements:
            if element.codeElement in couplages_criteres_par_element and couplages_criteres_par_element[element.codeElement]:
                # Sélectionner un couplage critère valide aléatoirement
                couplage_critere = random.choice(couplages_criteres_par_element[element.codeElement])
                solution_data.append(couplage_critere.to_dict())  # Convertir en dictionnaire
            else:
                # Si aucun couplageCritere n'est disponible, on garde l'ID de l'Element seul
                solution_data.append(element.codeElement)

        # Vérifier si la solution respecte les contraintes
        if verifier_contraintes_solution(solution_data, contraintes):
            # Évaluer la fitness de la solution
            fitness_score = evaluer_fitness(solution_data, objectifs)
            
            # Créer un dictionnaire structuré pour chaque solution
            solution_dict = {
                'data': solution_data,
                'objectifs': fitness_score  # Un dictionnaire avec les scores par objectif
            }
            
            # Ajouter la solution au format dictionnaire à la population
            population.append(solution_dict)
            print(f"Solution {len(population)} ajoutée avec fitness: {fitness_score}")

    if len(population) < taille_population:
        print(f"Attention: Seulement {len(population)} solutions valides trouvées sur {taille_population} demandées après {tentatives} tentatives")
    else:
        print(f"Population initiale de {taille_population} solutions générée avec succès")
    return population
#fitness
def evaluer_fitness(solution, objectifs):
    score = {}

    for objectif in objectifs:
        critere = objectif.idCritere
        critere_score = 0.0  # Initialiser en float

        for element_solution in solution:
            if 'valeur' not in element_solution:
                continue  # Ignorer si pas de valeur

            try:
                valeur = json.loads(element_solution['valeur'])  # Charger JSON en dict
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON pour {element_solution['valeur']}")
                continue

            critere_valeur = valeur.get(critere.nom, 0)  # Récupérer la valeur du critère
            if critere_valeur is None:
                critere_valeur = 0.0  # Éviter TypeError

            critere_score += float(critere_valeur)  # S'assurer que c'est un float

        score[critere.nom] = critere_score if objectif.type == 'max' else -critere_score

    return score  # Doit être un dict


#Sélection des parents (GA)
def dominance(s1, s2):
    """
    Vérifie si la solution s1 domine s2 dans une optimisation multicritère.
    """
    if not isinstance(s1, dict) or not isinstance(s2, dict):
        raise TypeError("Les arguments doivent être des dictionnaires")
    
    if 'objectifs' not in s1 or 'objectifs' not in s2:
        raise ValueError("Les solutions doivent contenir la clé 'objectifs'")
    
    # Handle objectifs as dictionaries (which they appear to be from evaluer_fitness)
    s1_obj = s1['objectifs']
    s2_obj = s2['objectifs']
    
    if not isinstance(s1_obj, dict) or not isinstance(s2_obj, dict):
        raise TypeError("'objectifs' doivent être des dictionnaires")
    
    # Check that s1 and s2 have the same objective keys
    if set(s1_obj.keys()) != set(s2_obj.keys()):
        raise ValueError("Les objectifs des solutions ne correspondent pas")
    
    # Check dominance
    at_least_one_better = False
    for key in s1_obj:
        if s1_obj[key] < s2_obj[key]:  # Assuming lower is better (for minimization)
            return False  # s1 is worse in at least one objective
        elif s1_obj[key] > s2_obj[key]:
            at_least_one_better = True  # s1 is better in at least one objective
    
    return at_least_one_better  # s1 dominates s2 if it's better in at least one objective

def non_dominated_sort(population):
    """
    Effectue le tri non dominé et retourne les fronts de Pareto.
    """
    fronts = []
    domination_counts = {i: 0 for i in range(len(population))}
    dominated_solutions = {i: [] for i in range(len(population))}

    for i in range(len(population)):
        for j in range(len(population)):
            if i != j:
                if dominance(population[i], population[j]):
                    dominated_solutions[i].append(j)
                elif dominance(population[j], population[i]):
                    domination_counts[i] += 1
        
        if domination_counts[i] == 0:
            if len(fronts) == 0:
                fronts.append([])
            fronts[0].append(i)
    
    index = 0
    while len(fronts[index]) > 0:
        next_front = []
        for i in fronts[index]:
            for j in dominated_solutions[i]:
                domination_counts[j] -= 1
                if domination_counts[j] == 0:
                    next_front.append(j)
        index += 1
        fronts.append(next_front)
    
    return fronts[:-1]

def crowding_distance(front, population):
    """
    Calcule la distance de crowding pour favoriser la diversité.
    """
    distance = {i: 0 for i in front}
    
    # Get the objective names from the first solution
    objective_names = list(population[0]['objectifs'].keys())
    
    for objective_name in objective_names:
        # Sort based on the specific objective name
        sorted_front = sorted(front, key=lambda i: population[i]['objectifs'][objective_name])
        
        # Set infinite distance for boundary points
        distance[sorted_front[0]] = float('inf')
        distance[sorted_front[-1]] = float('inf')
        
        min_val = population[sorted_front[0]]['objectifs'][objective_name]
        max_val = population[sorted_front[-1]]['objectifs'][objective_name]
        
        if max_val == min_val:
            continue
        
        # Calculate crowding distance for intermediate points
        for k in range(1, len(sorted_front) - 1):
            distance[sorted_front[k]] += (
                population[sorted_front[k+1]]['objectifs'][objective_name] - 
                population[sorted_front[k-1]]['objectifs'][objective_name]
            ) / (max_val - min_val)
    
    return distance
def selection_nsga2(population, nb_parents):
    """
    Sélectionne les parents en utilisant NSGA-II (fronts de Pareto + crowding distance).
    """
    fronts = non_dominated_sort(population)
    selected_parents = []
    
    for front in fronts:
        if len(selected_parents) + len(front) <= nb_parents:
            selected_parents.extend(front)
        else:
            distances = crowding_distance(front, population)
            sorted_front = sorted(front, key=lambda i: distances[i], reverse=True)
            selected_parents.extend(sorted_front[:nb_parents - len(selected_parents)])
            break

    return [population[i] for i in selected_parents]


#croisement
def croisement(parent1, parent2):
    """
    Effectue un croisement entre deux parents pour créer un enfant.
    """
    # Vérifier que les deux parents ont suffisamment d'éléments pour un croisement
    if len(parent1['data']) < 2 or len(parent2['data']) < 2:
        raise ValueError("Les parents doivent avoir plus d'un élément dans 'data' pour effectuer un croisement")

    # Générer un point de croisement valide
    point_croisement = random.randint(1, len(parent1['data']) - 1)

    # Effectuer le croisement (exemple de logique simple, à adapter selon ton besoin)
    enfant = {
        'data': parent1['data'][:point_croisement] + parent2['data'][point_croisement:],
        'objectifs': evaluer_fitness(parent1['data'][:point_croisement] + parent2['data'][point_croisement:], Objectif.objects.all())
    }
    return enfant


#mutation
def mutation(solution, mutation_rate=0.1):
    """
    Effectue une mutation sur une solution donnée avec un taux de mutation donné.
    """
    print("Données avant mutation:", solution['data'])  # Affiche les données avant mutation
    
    if 'data' not in solution:
        raise ValueError("La solution doit contenir la clé 'data'")

    # Vérifier la structure des données
    for elem in solution['data']:
        if not isinstance(elem, dict):
            raise TypeError(f"Un élément de 'data' n'est pas un dictionnaire: {elem}")

    # Appliquer la mutation sur les données
    for i in range(len(solution['data'])):
        if random.random() < mutation_rate:
            # Effectuer une mutation, par exemple changer 'couplage'
            solution['data'][i] = random.choice(Element.objects.all()).codeElement

    # Supprimer les doublons après mutation
    seen = set()
    solution['data'] = [elem for elem in solution['data'] if isinstance(elem, dict) and elem['couplage'] not in seen and not seen.add(elem['couplage'])]

    # Recalculer les objectifs après mutation
    solution['objectifs'] = evaluer_fitness(solution['data'], Objectif.objects.all())

    print("Données après mutation:", solution['data'])  # Affiche les données après mutation
    
    return solution



def generer_nouvelle_population(population, nb_enfants, mutation_rate=0.1):
    nouvelle_population = []

    # Sélectionner les parents
    parents = selection_nsga2(population, nb_enfants)

    # Créer des enfants par croisement et mutation
    while len(nouvelle_population) < nb_enfants:
        # Sélectionner deux parents aléatoires
        parent1, parent2 = random.sample(parents, 2)

        # Effectuer un croisement pour générer un enfant
        enfant = croisement(parent1, parent2)

        # Appliquer une mutation à l'enfant
        enfant_muté = mutation(enfant, mutation_rate)

        # Ajouter l'enfant à la nouvelle population
        nouvelle_population.append(enfant_muté)

    return nouvelle_population


#Boucle principale pour l'agorithme genetique
def evolution_genetique(taille_population, contraintes, generations=10, mutation_rate=0.1):
    # Générer la population initiale
    population = generer_population_initiale(taille_population, contraintes)
    print("popo generee")
    print(population[0])

    for generation in range(generations):
        print(f"===== Génération {generation + 1} =====")

        # Sélection des parents avec NSGA-II
        nb_parents = min(2, len(population))  # Nombre de parents à sélectionner
        parents = selection_nsga2(population, nb_parents)

        # Génération d'une nouvelle population
        nouvelle_population = generer_nouvelle_population(parents, taille_population, mutation_rate)

        # Mise à jour de la population
        population = nouvelle_population
        print(f"populatation1:{population[1]}")
        print(f"populatation2:{population[2]}")
        print(f"Population mise à jour: {len(population)} individus")

    print("Évolution terminée.")
    return population
