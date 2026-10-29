from django.db import models


class Auteur(models.Model):
    nom = models.CharField(max_length=150)
    biographie = models.TextField(blank=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Livre(models.Model):
    titre = models.CharField(max_length=200)

    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.PROTECT,
        related_name='livres'
    )

    isbn = models.CharField(
        max_length=20,
        blank=True
    )

    description = models.TextField(blank=True)

    date_publication = models.DateField(
        null=True,
        blank=True
    )

    date_ajout = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['titre']

    def __str__(self):
        return self.titre