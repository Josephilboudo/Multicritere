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
    description = models.CharField(max_length=255)
    expression = models.TextField()  # Expression mathématique ou logique
    
    def __str__(self):
        return self.nom
    
    
class CouplageCritere(models.Model):
    idValeur = models.AutoField(primary_key=True)
    couplage = models.ForeignKey(Couplage, on_delete=models.CASCADE)
    valeur= models.JSONField()
    
class Contrainte(models.Model):
    idContrainte = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    description = models.TextField()
    idCriterefk = models.ForeignKey(Critere, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nom
    
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
    
  