from django.shortcuts import render, redirect, get_object_or_404
from article.models import Article
from stock.models import Stock
from rapport.models import Rapport
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from functools import wraps
from django.core.exceptions import PermissionDenied
from stockmanagement.middleware import role_required  

# def role_required(allowed_roles): 
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             if request.user.groups.filter(name__in=allowed_roles).exists():
#                 return view_func(request, *args, **kwargs)
#             raise PermissionDenied
#         return wrapper
#     return decorator

def home_view(request):
    return render(request, 'homepage.html')

def loginpage_view(request):
    return render(request, 'loginpage.html')

def fournisseur_view(request):
    return render(request,'fournisseur.html')

# Helper to disable cache
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Now apply everywhere
@never_cache
@login_required(login_url='/loginpage/')
@role_required(['stock_manager'])
def article_view(request):
    if not request.user.is_authenticated :
        return redirect('/loginpage/')
    response = render(request, 'articles.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['stock_manager'])
def stock_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'stocks.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def commands_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'commandes.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['stock_manager'])
def rapport_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'rapports.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['stock_manager'])
def historique_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'historique.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def gestionnaire_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'gestionnaire.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def employe_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'employe.html')
    return disable_cache(response)

# @never_cache
# @login_required(login_url='/loginpage/')
# @role_required(['employe'])
# def liststocks_view(request):
#     if not request.user.is_authenticated:
#         return redirect('/loginpage/')
#     response = render(request, 'liststocks.html')
#     return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['employe'])
def listarticles_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'listarticles.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['employe'])
def listcommands_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'listcommands.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_article_view(request, article_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    article = get_object_or_404(Article, pk=article_id)
    response = render(request, 'article_form.html', {'article': article})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_stock_view(request, stock_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    stock = get_object_or_404(Stock, id=stock_id)
    response = render(request, 'stock_form.html', {'stock': stock})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_rapport_view(request, rapport_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    rapport = get_object_or_404(Rapport, id=rapport_id)
    stocks = Stock.objects.all()
    response = render(request, 'rapport_form.html', {'rapport': rapport,'stocks': stocks})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_stock_form_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'stock_form.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def search_article_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'searcharticle.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['stock_manager'])
def get_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'dashboard.html')
    return disable_cache(response)
