import random

from ij.calcul import verifier_contraintes_solution
from .models import CouplageCritere, Element, Couplage
from collections import defaultdict
from datetime import datetime

def generer_population_initiale(taille_population, contraintes):
    # Récupérer tous les éléments (tâches)
    elements = list(Element.objects.all())

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
    return population
