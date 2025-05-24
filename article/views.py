from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from article.models import Article
from django.db.models import Q
from user.models import UserProfile
from stockmanagement.middleware import role_required  # Add this import

def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['employe'])  # Use the decorator correctly
def list_articles(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    articles = Article.objects.all()
    response = render(request, 'listarticles.html', {'articles': articles})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_articles(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    articles = Article.objects.all()
    response = render(request, 'articles.html', {'articles': articles})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def create_article(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        references = request.POST.get('references')
        categorie = request.POST.get('categorie')
        prix = request.POST.get('prix')
        description = request.POST.get('description')

        if not nom or quantite is None:
            messages.error(request, "Nom et Quantité sont requis.")
            response = render(request, 'articles.html')
            return disable_cache(response)

        try:
            quantite = int(quantite)
        except ValueError:
            messages.error(request, "Quantité doit être un entier.")
            response = render(request, 'articles.html')
            return disable_cache(response)

        try:
            prix = float(prix) if prix else None
        except ValueError:
            messages.error(request, "Prix invalide.")
            response = render(request, 'articles.html')
            return disable_cache(response)

        etat = 'en_stock' if quantite > 0 else 'hors_stock'

        Article.objects.create(
            nom=nom,
            quantite=quantite,
            references=references,
            categorie=categorie,
            prix=prix,
            description=description,
            etat=etat
        )

        messages.success(request, "Article ajouté avec succès.")
        return redirect('get_articles')

    response = render(request, 'articles.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_article(request, article_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        references = request.POST.get('references')
        categorie = request.POST.get('categorie')
        prix = request.POST.get('prix')
        description = request.POST.get('description')

        if not nom or quantite is None:
            return HttpResponse("Champs requis manquants", status=400)

        try:
            quantite = int(quantite)
        except ValueError:
            return HttpResponse("Quantité invalide", status=400)

        try:
            prix = float(prix) if prix else None
        except ValueError:
            return HttpResponse("Prix invalide", status=400)

        article.nom = nom
        article.quantite = quantite
        article.references = references
        article.categorie = categorie
        article.prix = prix
        article.description = description
        article.etat = 'en_stock' if quantite > 0 else 'hors_stock'

        article.save()
        return redirect('get_articles')

    response = render(request, 'article_form.html', {'article': article})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def delete_article(request, article_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article supprimé avec succès.")
        return redirect('get_articles')

    response = render(request, 'article_confirm_delete.html', {'article': article})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def search_articles(request):
    query = request.GET.get('query', '').strip()
    articles = Article.objects.none()

    if query:
        articles = Article.objects.filter(
            Q(nom__icontains=query) | Q(references__icontains=query)
        )

    response = render(request, 'searcharticle.html', {'articles': articles, 'query': query})
    return disable_cache(response)
