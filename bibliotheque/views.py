from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LivreForm
from .models import Livre


def accueil(request):
    recherche = request.GET.get('q', '').strip()
    livres = Livre.objects.select_related('auteur').all()

    if recherche:
        livres = livres.filter(
            Q(titre__icontains=recherche)
            | Q(auteur__nom__icontains=recherche)
            | Q(isbn__icontains=recherche)
        )

    paginator = Paginator(livres, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'bibliotheque/accueil.html',
        {
            'page_obj': page_obj,
            'recherche': recherche,
        },
    )


def detail_livre(request, livre_id):
    livre = get_object_or_404(
        Livre.objects.select_related('auteur'),
        pk=livre_id,
    )

    return render(
        request,
        'bibliotheque/detail.html',
        {'livre': livre},
    )


@staff_member_required
def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Le livre a été ajouté avec succès !",
            )
            return redirect('bibliotheque:accueil')
    else:
        form = LivreForm()

    return render(
        request,
        'bibliotheque/formulaire.html',
        {
            'form': form,
            'titre_page': 'Ajouter un livre',
        },
    )


@staff_member_required
def modifier_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)

    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Le livre a été modifié avec succès !",
            )
            return redirect(
                'bibliotheque:detail_livre',
                livre_id=livre.id,
            )
    else:
        form = LivreForm(instance=livre)

    return render(
        request,
        'bibliotheque/formulaire.html',
        {
            'form': form,
            'titre_page': 'Modifier un livre',
        },
    )


@staff_member_required
def supprimer_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)

    if request.method == 'POST':
        titre_livre = livre.titre
        livre.delete()

        messages.success(
            request,
            f"Le livre « {titre_livre} » a été supprimé avec succès !",
        )

        return redirect('bibliotheque:accueil')

    return render(
        request,
        'bibliotheque/confirmer_suppression.html',
        {'livre': livre},
    )
