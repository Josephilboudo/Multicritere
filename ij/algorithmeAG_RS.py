def appliquer_recuit_sur_population(population, ensemble_possibilites, temperature_initiale=100, refroidissement=0.95, iterations=1000):
    """Applique le recuit simulé sur chaque individu de la population générée par le GA"""
    population_amelioree = []
    for individu in population:
        solution_amelioree = recuit_simule(individu, ensemble_possibilites, temperature_initiale, refroidissement, iterations)
        population_amelioree.append(solution_amelioree)
    
    return population_amelioree