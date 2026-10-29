from django.contrib import admin
from .models import Auteur, Livre


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'auteur',
        'isbn',
        'date_publication',
        'date_ajout',
    )

    search_fields = (
        'titre',
        'auteur__nom',
        'isbn',
    )

    list_filter = ('date_publication',)