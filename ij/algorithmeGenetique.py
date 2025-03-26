from copy import deepcopy
import json
import math
import random

from ij.calcul import verifier_contraintes_solution
from .models import CouplageCritere, Element, Couplage, Objectif
from collections import defaultdict
from datetime import datetime

def generer_population_initiale(taille_population, contraintes):
    # Récupérer tous les éléments (tâches)
    elements = list(Element.objects.all())
    objectifs = Objectif.objects.all()
    taille_population=100

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
def croisement_intelligent(parent1, parent2, contraintes):
    """
    Croisement qui préserve la structure et garantit la validité
    """
    # Générer plusieurs points de croisement
    nb_points = random.randint(1, min(len(parent1['data']) - 1, 3))
    points = sorted(random.sample(range(1, len(parent1['data'])), nb_points))
    
    # Construire l'enfant avec segments alternés
    enfant_data = []
    source_parent = parent1
    
    for i in range(len(parent1['data'])):
        if i in points:
            # Alterner la source du parent
            source_parent = parent2 if source_parent == parent1 else parent1
        
        enfant_data.append(source_parent['data'][i])
    
    # Vérifier les contraintes
    if verifier_contraintes_solution(enfant_data, contraintes):
        enfant = {
            'data': enfant_data,
            'objectifs': evaluer_fitness(enfant_data, Objectif.objects.all())
        }
        return enfant
    
    # Fallback : retourner un parent si les contraintes ne sont pas respectées
    return random.choice([parent1, parent2])

#mutation
def mutation_intelligente(solution, contraintes):
    """
    Mutation qui préserve la structure et garantit la validité
    """
    # Copie profonde pour éviter les modifications directes
    mutated_solution = deepcopy(solution)
    
    # Récupérer tous les éléments disponibles
    elements = list(Element.objects.all())
    
    # Sélectionner un sous-ensemble d'éléments à muter
    nb_mutations = max(1, int(len(mutated_solution['data']) * 0.2))  # Muter 20% des éléments
    indices_mutation = random.sample(range(len(mutated_solution['data'])), nb_mutations)
    
    for idx in indices_mutation:
        # Filtrer les éléments candidats par contraintes
        candidats = [
            elem for elem in elements 
            if elem.codeElement.startswith(mutated_solution['data'][idx]['couplage'].split('_')[0])
        ]
        
        if candidats:
            # Sélection aléatoire parmi les candidats valides
            nouvel_element = random.choice(candidats)
            mutated_solution['data'][idx]['couplage'] = nouvel_element.codeElement
    
    # Vérifier et corriger les contraintes
    if verifier_contraintes_solution(mutated_solution['data'], contraintes):
        # Recalculer les objectifs
        mutated_solution['objectifs'] = evaluer_fitness(
            mutated_solution['data'], 
            Objectif.objects.all()
        )
        return mutated_solution
    
    # Retourner la solution originale si la mutation invalide les contraintes
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
        #print(f"enfant a mute:{enfant}")
        # Appliquer une mutation à l'enfant
        enfant_muté = mutation(enfant, mutation_rate)
        #print(f"enfant mute:{enfant_muté}")

        # Ajouter l'enfant à la nouvelle population
        nouvelle_population.append(enfant_muté)

    return nouvelle_population


#Boucle principale pour l'agorithme genetique
def evolution_genetique(
    taille_population, 
    contraintes, 
    generations=20, 
    mutation_rate=0.2
):
    # Générer une population initiale plus diversifiée
    population = generer_population_initiale(
        taille_population * 2,  # Plus de candidats initiaux
        contraintes
    )[:taille_population]
    
    # Historique pour suivre la diversité
    historique_diversite = []
    
    for generation in range(generations):
        print(f"===== Génération {generation + 1} =====")
        
        # Sélection des meilleurs et des plus diversifiés
        nouvelle_population = []
        
        # Tri non dominé pour identifier les fronts de Pareto
        fronts = non_dominated_sort(population)
        
        # Sélectionner des solutions à partir des premiers fronts
        for front in fronts:
            front_solutions = [population[i] for i in front]
            
            # Ajouter des solutions jusqu'à atteindre la taille de population
            while len(nouvelle_population) < taille_population and front_solutions:
                # Sélection aléatoire pondérée
                solution = random.choice(front_solutions)
                front_solutions.remove(solution)
                nouvelle_population.append(solution)
        
        # Générer de nouveaux individus par croisement et mutation
        while len(nouvelle_population) < taille_population:
            # Sélection des parents
            parent1, parent2 = random.sample(population, 2)
            
            # Croisement
            enfant = croisement_intelligent(parent1, parent2, contraintes)
            
            # Mutation conditionnelle
            if random.random() < mutation_rate:
                enfant = mutation_intelligente(enfant, contraintes)
            
            nouvelle_population.append(enfant)
        
        # Mettre à jour la population
        population = nouvelle_population
        
        # Calculer et suivre la diversité
        diversite = len(set(tuple(sorted(p['objectifs'].items())) for p in population))
        historique_diversite.append(diversite)
        print(f"Diversité des objectifs : {diversite}")
    
    # Optionnel : tracer l'évolution de la diversité
    # plot_diversite(historique_diversite)
    print(f"pop1: {population[1]}\n")
    print(f"pop2: {population[2]}\n")
    print(f"pop3: {population[3]}\n")
    return population


def croisement_multipoint(parent1, parent2):
    """
    Croisement multi-points pour plus de diversité
    """
    points_croisement = sorted(
        random.sample(range(1, len(parent1['data'])), 2)
    )
    
    enfant1 = {
        'data': (
            parent1['data'][:points_croisement[0]] + 
            parent2['data'][points_croisement[0]:points_croisement[1]] + 
            parent1['data'][points_croisement[1]:]
        ),
        'objectifs': None  # Sera calculé après
    }
    
    enfant1['objectifs'] = evaluer_fitness(
        enfant1['data'], 
        Objectif.objects.all()
    )
    
    return enfant1
def selection_nsga2_avec_diversite(population, nb_parents):
    """
    Sélection avec préservation de la diversité
    Gère les cas de distances de crowding problématiques
    """
    fronts = non_dominated_sort(population)
    selected_parents = []
    
    for front in fronts:
        if len(selected_parents) + len(front) <= nb_parents:
            # Ajouter des éléments aléatoires du front pour diversité
            random.shuffle(front)
            selected_parents.extend(front)
        else:
            # Sélection aléatoire pondérée avec gestion des poids
            distances = crowding_distance(front, population)
            
            # Nettoyer et normaliser les distances
            cleaned_distances = []
            for i in front:
                dist = distances[i]
                # Convertir les valeurs infinies ou NaN en grande valeur
                if dist == float('inf') or math.isnan(dist):
                    cleaned_distances.append(1000)  # Grande valeur constante
                else:
                    cleaned_distances.append(max(dist, 0.001))  # Éviter les zéros
            
            # Normaliser les poids
            total_weight = sum(cleaned_distances)
            probabilities = [d / total_weight for d in cleaned_distances]
            
            try:
                selected = random.choices(
                    front, 
                    weights=probabilities, 
                    k=nb_parents - len(selected_parents)
                )
                selected_parents.extend(selected)
            except ValueError:
                # Fallback: sélection aléatoire si problème de poids
                selected = random.sample(
                    front, 
                    k=nb_parents - len(selected_parents)
                )
                selected_parents.extend(selected)
            
            break

    return [population[i] for i in selected_parents]