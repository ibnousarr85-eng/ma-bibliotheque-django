from django import forms
from .models import Livre

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = [
            'titre',
            'auteur',
            'isbn',
            'description',
            'date_publication',
        ]

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du livre'
            }),
            'auteur': forms.Select(attrs={
                'class': 'form-control'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro ISBN'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du livre',
                'rows': 4
            }),
            'date_publication': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }