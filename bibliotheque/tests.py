from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Auteur, Livre


class CatalogueTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auteur = Auteur.objects.create(
            nom='Aminata Diallo',
            biographie='Autrice fictive.',
        )
        cls.livre = Livre.objects.create(
            titre='Les chemins du fleuve',
            auteur=cls.auteur,
            isbn='9781234567890',
        )

    def test_liste_affiche_les_livres(self):
        response = self.client.get(reverse('bibliotheque:accueil'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livre.titre)
        self.assertContains(response, self.auteur.nom)

    def test_recherche_par_titre_auteur_et_isbn(self):
        for terme in ('chemins', 'Aminata', '9781234567890'):
            with self.subTest(terme=terme):
                response = self.client.get(
                    reverse('bibliotheque:accueil'),
                    {'q': terme},
                )
                self.assertContains(response, self.livre.titre)

        response = self.client.get(
            reverse('bibliotheque:accueil'),
            {'q': 'introuvable'},
        )
        self.assertContains(response, 'Aucun livre ne correspond')

    def test_detail_livre_et_404(self):
        response = self.client.get(
            reverse('bibliotheque:detail_livre', args=[self.livre.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livre.titre)

        response = self.client.get(
            reverse('bibliotheque:detail_livre', args=[99999])
        )
        self.assertEqual(response.status_code, 404)


class GestionLivreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auteur = Auteur.objects.create(nom='Mamadou Ba')
        cls.livre = Livre.objects.create(
            titre='Le jardin secret',
            auteur=cls.auteur,
        )
        user_model = get_user_model()
        cls.utilisateur = user_model.objects.create_user(
            username='lecteur',
            password='test-password-123',
        )
        cls.personnel = user_model.objects.create_user(
            username='personnel',
            password='test-password-123',
            is_staff=True,
        )

    def test_pages_de_gestion_refusees_aux_non_personnels(self):
        urls = (
            reverse('bibliotheque:ajouter_livre'),
            reverse('bibliotheque:modifier_livre', args=[self.livre.pk]),
            reverse('bibliotheque:supprimer_livre', args=[self.livre.pk]),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        self.client.force_login(self.utilisateur)
        for url in urls:
            with self.subTest(url=url, user='lecteur'):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_personnel_peut_ajouter_un_livre(self):
        self.client.force_login(self.personnel)
        response = self.client.post(
            reverse('bibliotheque:ajouter_livre'),
            {
                'titre': 'Une nouvelle histoire',
                'auteur': self.auteur.pk,
                'isbn': '',
                'description': '',
                'date_publication': '',
            },
        )

        self.assertRedirects(response, reverse('bibliotheque:accueil'))
        self.assertTrue(
            Livre.objects.filter(titre='Une nouvelle histoire').exists()
        )

    def test_suppression_est_confirmee_en_post(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.personnel)
        url = reverse('bibliotheque:supprimer_livre', args=[self.livre.pk])

        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Livre.objects.filter(pk=self.livre.pk).exists())

        response = client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Livre.objects.filter(pk=self.livre.pk).exists())

        csrf_token = response.cookies.get('csrftoken')
        if csrf_token is None:
            response = client.get(url)
            csrf_token = response.cookies['csrftoken']

        response = client.post(url, HTTP_X_CSRFTOKEN=csrf_token.value)
        self.assertRedirects(response, reverse('bibliotheque:accueil'))
        self.assertFalse(Livre.objects.filter(pk=self.livre.pk).exists())

    def test_un_auteur_avec_des_livres_ne_peut_pas_etre_supprime(self):
        from django.db.models import ProtectedError

        with self.assertRaises(ProtectedError):
            self.auteur.delete()

    def test_formulaire_affiche_les_erreurs(self):
        self.client.force_login(self.personnel)
        response = self.client.post(
            reverse('bibliotheque:ajouter_livre'),
            {'titre': '', 'auteur': self.auteur.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ce champ est obligatoire.')


class DonneesDemoTests(TestCase):
    fixtures = ['donnees_demo']

    def test_fixture_charge_les_auteurs_et_livres(self):
        self.assertEqual(Auteur.objects.count(), 5)
        self.assertEqual(Livre.objects.count(), 20)
        self.assertContains(
            self.client.get(
                reverse('bibliotheque:accueil'),
                {'q': 'Une si longue lettre'},
            ),
            'Une si longue lettre',
        )

    def test_catalogue_demo_est_pagine_sur_quatre_pages(self):
        response = self.client.get(reverse('bibliotheque:accueil'))

        self.assertEqual(response.context['page_obj'].paginator.count, 20)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 4)

    def test_auteurs_demo_sont_reels_et_biographies_documentees(self):
        auteur = Auteur.objects.get(nom='Mariama Bâ')
        self.assertIn('Dakar en 1929', auteur.biographie)
        self.assertIn('Une si longue lettre', auteur.biographie)
        self.assertFalse(Auteur.objects.filter(nom='Lina Mbaye').exists())

    def test_livres_demo_sont_attribues_aux_bons_auteurs(self):
        self.assertEqual(
            Livre.objects.get(titre='La Grève des bàttu').auteur.nom,
            'Aminata Sow Fall',
        )
        self.assertEqual(
            Livre.objects.get(titre='Murambi, le livre des ossements').auteur.nom,
            'Boubacar Boris Diop',
        )
