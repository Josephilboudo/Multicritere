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
    for _ in range(taille_population):
        solution = []

        for element in elements:
            if element.codeElement in couplages_criteres_par_element and couplages_criteres_par_element[element.codeElement]:
                # Sélectionner un couplage critère valide aléatoirement
                couplage_critere = random.choice(couplages_criteres_par_element[element.codeElement])
                solution.append(couplage_critere.to_dict())  # Convertir en dictionnaire
            else:
                # Si aucun couplageCritere n'est disponible, on garde l'ID de l'Element seul
                solution.append(element.codeElement)

        # Vérifier si la solution respecte les contraintes
        if verifier_contraintes_solution(solution, contraintes):
            population.append(solution)  # Ajouter la solution à la population si elle respecte les contraintes
        else:
            continue  # Si la solution ne respecte pas les contraintes, on passe à la suivante
    print(population[0])
    print(len(population))
    for solution in population:
        fitness_score = evaluer_fitness(solution, objectifs)
        print(f"Fitness de la solution : {fitness_score}")
    return population



#fitness
from django.db.models import F

import json

def evaluer_fitness(solution, objectifs):
    """
    Fonction de fitness pour évaluer une solution en fonction des objectifs.
    :param solution: La solution à évaluer (liste d'éléments).
    :param objectifs: Liste des objectifs à optimiser (max ou min).
    :return: Score de la solution.
    """
    score = 0

    # Parcourir chaque objectif
    for objectif in objectifs:
        critere = objectif.idCritere
        critere_score = 0

        for element_solution in solution:
            couplage_id = element_solution['couplage']
            valeur_str = element_solution['valeur']  # Récupère la valeur sous forme de string JSON

            try:
                valeur = json.loads(valeur_str)  # Convertir en dictionnaire
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON pour {valeur_str}")
                continue  # Ignorer cette valeur et passer à la suivante

            critere_valeur = valeur.get(critere.nom)  # Accéder à la valeur du critère

            if critere_valeur is not None:
                critere_score += critere_valeur

        # Maximiser ou minimiser en fonction du type d'objectif
        if objectif.type == 'max':
            score += critere_score
        elif objectif.type == 'min':
            score -= critere_score

    return score
