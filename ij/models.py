from django.db import models

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
    expression = models.CharField(max_length=255)  # Expression mathématique ou logique
    poids = models.FloatField(default=1.0)  # Poids du critère
    
    def __str__(self):
        return self.nom
    
class Contrainte(models.Model):
    idContrainte = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.nom
    
class Objectif(models.Model):
    idObjectif = models.AutoField(primary_key=True)
    description = models.TextField()
    
    def __str__(self):
        return self.description
  
class Solution(models.Model):
    idSolution = models.AutoField(primary_key=True)
    statut = models.TextField()
    couplages = models.ManyToManyField(Couplage, related_name="solutions")
    solution = models.ManyToManyField(Objectif, related_name="solutions")
    
    def __str__(self):
        return self.statut
    
  