from django import forms

class FichierCSVForm(forms.Form):
    csv_file = forms.FileField(label="Choisir un fichier CSV")
