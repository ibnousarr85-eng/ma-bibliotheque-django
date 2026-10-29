# Catalogue de livres BEMTECH

Application Django en français permettant de consulter et rechercher des livres. Le personnel (`is_staff`) peut ajouter, modifier et supprimer des fiches ; l'administration Django permet aussi de gérer les auteurs et les livres.

## Prérequis

- Python 3.10 ou plus récent
- `pip`

## Installation

Depuis le dossier du projet, créez puis activez un environnement virtuel :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Sous Windows, si PowerShell bloque l'activation, utilisez directement `.\.venv\Scripts\python.exe` à la place de `python`.

En développement, aucun réglage supplémentaire n'est nécessaire. Pour un déploiement, définissez `DJANGO_DEBUG=False` et fournissez une clé secrète via `DJANGO_SECRET_KEY` (par exemple, générez-en une avec `python -c "import secrets; print(secrets.token_urlsafe(50))"`). Ne publiez jamais cette clé.

## Préparer la base et charger les données démo

```powershell
python manage.py migrate
python manage.py loaddata donnees_demo
```

La fixture `bibliotheque/fixtures/donnees_demo.json` contient exactement vingt livres publiés et cinq auteurs sénégalais réels, avec des biographies et des descriptions rédigées pour le catalogue. Elle remplace les anciennes entrées fictives grâce aux identifiants fixes. Les ISBN restent vides lorsqu'ils ne sont pas vérifiés plutôt que d'afficher de faux numéros.

Les notices biographiques et bibliographies ont été vérifiées à partir des références suivantes :

- [Mariama Bâ](https://en.wikipedia.org/wiki/Mariama_B%C3%A2)
- [Cheikh Hamidou Kane](https://en.wikipedia.org/wiki/Cheikh_Hamidou_Kane)
- [Ousmane Sembène](https://en.wikipedia.org/wiki/Ousmane_Semb%C3%A8ne)
- [Aminata Sow Fall](https://en.wikipedia.org/wiki/Aminata_Sow_Fall)
- [Boubacar Boris Diop](https://en.wikipedia.org/wiki/Boubacar_Boris_Diop)

## Créer un compte administrateur

```powershell
python manage.py createsuperuser
```

Le compte administrateur peut gérer les données dans `/admin/`. Pour utiliser les pages d'ajout, de modification et de suppression sur le site, un compte doit avoir le statut « personnel » (`is_staff`). `createsuperuser` attribue ce statut automatiquement ; un administrateur peut également le donner depuis l'administration à un autre compte.

## Lancer le serveur

```powershell
python manage.py runserver
```

Ouvrez `http://127.0.0.1:8000/` pour le catalogue, `http://127.0.0.1:8000/admin/` pour l'administration, et `http://127.0.0.1:8000/accounts/login/` pour vous connecter.

## Tests

```powershell
python manage.py test
```
