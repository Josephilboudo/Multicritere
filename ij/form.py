from django import forms
from .models import Element, Ressource

class FichierCSVForm(forms.Form):
    csv_file = forms.FileField(label="Choisir un fichier CSV")
    
    

class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['codeElement', 'nom']
