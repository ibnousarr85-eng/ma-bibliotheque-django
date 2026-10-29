from django.urls import path
from . import views

app_name = 'bibliotheque'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('livre/<int:livre_id>/', views.detail_livre, name='detail_livre'),
    path('livre/ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('livre/<int:livre_id>/modifier/', views.modifier_livre, name='modifier_livre'),
    path('livre/<int:livre_id>/supprimer/', views.supprimer_livre, name='supprimer_livre'),
]