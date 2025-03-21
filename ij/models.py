from django.db import models
from collections import defaultdict

class Element(models.Model):  
    codeElement = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.CharField(max_length=100, default="Aucune description")

    def __str__(self):
        return self.description
    
class Ressource(models.Model):  
    codeRessource = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.CharField(max_length=100, default="Aucune description")

    def __str__(self):
        return self.description

 
   
class Couplage(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
   # Clé primaire personnalisée
    id = models.CharField(max_length=255, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        # Générer la clé primaire en concaténant les IDs
        self.id = f"{self.element_id}_{self.ressource_id}"
        super().save(*args, **kwargs)
    
class Critere(models.Model):
    idCritere = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    expression = models.TextField()  # Expression sql
    
    def __str__(self):
        return self.nom
    
    
class CouplageCritere(models.Model):
    idValeur = models.AutoField(primary_key=True)
    couplage = models.ForeignKey(Couplage, on_delete=models.CASCADE)
    valeur= models.JSONField()
    

class Contrainte(models.Model):
    idContrainte = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    critere_cible = models.CharField(max_length=50)  # Nom du critère ciblé
    type = models.CharField(max_length=10)
    seuil = models.CharField(max_length=255)  # Peut être un critère ou une valeur
    estAppliqueSolution = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.critere_cible} {self.type} {self.seuil}"
    
    
class Objectif(models.Model):
    idObjectif = models.AutoField(primary_key=True)
    description = models.TextField()
    type = models.CharField(max_length=15)
    idCritere = models.ForeignKey(Critere, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.description
  
class Solution(models.Model):
    idSolution = models.AutoField(primary_key=True)
    statut = models.TextField()
    couplages = models.ManyToManyField(Couplage, related_name="solutions")
    solution = models.ManyToManyField(Objectif, related_name="solutions")
    
    def __str__(self):
        return self.statut
    
  
from collections import defaultdict

def verifier_contraintes_solution(solution, contraintes):
    # Dictionnaire pour regrouper les valeurs des critères par ressource
    aggregation_criteres = defaultdict(lambda: defaultdict(float))

    # Étape 1: Groupement des valeurs par ressource
    for couplage, valeur_criteres in solution:
        ressource = couplage.ressource  # Regroupement par ressource (ex: enseignant)
        for critere, valeur in valeur_criteres.items():
            aggregation_criteres[ressource][critere] += valeur  # Somme des valeurs par critère

    # Étape 2: Vérification des contraintes sur les critères agrégés
    for contrainte in contraintes:
        critere_cible = contrainte.critere_cible  # Ex: "volume_horaire"
        seuil = contrainte.seuil  # Ex: "volume_statutaire" ou valeur numérique
        type_contrainte = contrainte.type  # "max", "min", "egal"

        for ressource, criteres in aggregation_criteres.items():
            if critere_cible not in criteres:
                continue  # Passer à la ressource suivante si critère non trouvé

            valeur_totale = criteres[critere_cible]  # Somme du critère pour cette ressource

            # Si le seuil est un critère et non une valeur fixe, récupérer sa valeur agrégée
            try:
                seuil_numerique = float(seuil)
            except ValueError:
                if seuil in criteres:
                    seuil_numerique = float(criteres[seuil])
                else:
                    continue  # Seuil inconnu, on passe

            # Vérification de la contrainte
            if type_contrainte == "max" and valeur_totale > seuil_numerique:
                return False  # Contrainte violée
            elif type_contrainte == "min" and valeur_totale < seuil_numerique:
                return False  # Contrainte violée
            elif type_contrainte == "egal" and valeur_totale != seuil_numerique:
                return False  # Contrainte violée

    return True  # Toutes les contraintes sont respectées
