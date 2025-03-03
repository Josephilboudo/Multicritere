from django.db import models

class Element(models.Model):
    codeElement = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom
    
class Ressource(models.Model):
    codeRessource = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom
    
class Couplage(models.Model):
    element = models.ManyToManyField(Element, through='CouplageElementRessource', related_name="couplages")
    ressource = models.ManyToManyField(Ressource, through='CouplageElementRessource', related_name="couplages")
    cout = models.FloatField()
    
    def __str__(self):
        return self.cout
    
class CouplageElementRessource(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    couplage = models.ForeignKey(Couplage, on_delete=models.CASCADE)
    
class Critere(models.Model):
    idCritere = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    description = models.TextField()
    
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
    
  