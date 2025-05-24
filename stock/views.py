# stock/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from user.models import UserProfile
from article.models import Article
from stock.models import Stock
from django.db.models import Q
from django.utils import timezone
from stockmanagement.middleware import role_required

# Helper to disable caching
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['employe'])
def liststocks_view(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    response = render(request, 'liststocks.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_stocks(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stocks = Stock.objects.all()
    articles = Article.objects.all()

    response = render(request, 'stocks.html', {
        'stocks': stocks,
        'articles': articles,
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_stock_form(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stocks = Stock.objects.all()
    articles = Article.objects.all()

    response = render(request, 'stock_form.html', {  # <--- here 'stock_form.html'
        'stocks': stocks,
        'articles': articles,
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def list_stocks(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')

    stocks = Stock.objects.all()
    response = render(request, 'liststocks.html', {
        'stocks': stocks,
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def create_stock(request):
    if request.method == 'POST':
        article_id = request.POST.get('article')
        quantite = request.POST.get('quantiteDisponible')
        seuilAlerte = request.POST.get('seuilAlerte')
        type = request.POST.get('type')
        etatStock = request.POST.get('etatStock')
        date = request.POST.get('date')  # Capture the date

        try:
            # Retrieve the article object based on the ID
            article = Article.objects.get(id=article_id)
            quantite = int(quantite)
            seuilAlerte = int(seuilAlerte)
            date = timezone.datetime.strptime(date, '%Y-%m-%d').date()  # Convert the date string to a date object

            # Create a new Stock entry in the database
            Stock.objects.create(
                article=article,
                quantiteDisponible=quantite,
                seuilAlerte=seuilAlerte,
                type=type,
                etatStock=etatStock,
                utilisateur=request.user,
                date=date  # Save the date
            )

            # Redirect to the 'get_stocks' view after successful creation
            return redirect('get_stocks')

        except (ValueError, TypeError, Article.DoesNotExist) as e:
            # Handle errors and display them to the user
            return render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur dans les champs du formulaire: ' + str(e)
            })

    # If it's a GET request, show the form to the user
    return render(request, 'stocks.html', {
        'stocks': Stock.objects.all(),
        'articles': Article.objects.all()
    })


@never_cache
@login_required(login_url='/loginpage/')
def update_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':
        article_id = request.POST.get('article')
        quantite = request.POST.get('quantite')
        seuilAlerte = request.POST.get('seuilAlerte')
        type = request.POST.get('type')
        etatStock = request.POST.get('etatStock')

        try:
            article = Article.objects.get(id=article_id)
            quantite = int(quantite)
            seuilAlerte = int(seuilAlerte)

            stock.article = article
            stock.quantiteDisponible = quantite
            stock.seuilAlerte = seuilAlerte
            stock.type = type
            stock.etatStock = etatStock
            stock.utilisateur = request.user
            stock.date=timezone.now().date()
            stock.save()

            return redirect('get_stocks')

        except (ValueError, TypeError, Article.DoesNotExist):
            return render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur dans les champs du formulaire.'
            })

    return render(request, 'stock_form.html', {
        'stocks': Stock.objects.all(),
        'articles': Article.objects.all(),
        'stock': stock,
        'article': stock.article
    })

@never_cache
@login_required(login_url='/loginpage/')
def delete_stock(request, stock_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')

    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
    return redirect('get_stocks')

def search_stocks(request):
    query = request.GET.get('query', '').strip()

    stocks = Stock.objects.none()  # Default to empty queryset

    if query:
        # Search for stocks whose associated article's nom or references contain the query
        stocks = Stock.objects.filter(
            Q(article__nom__icontains=query) | Q(article__references__icontains=query)
        )

    return render(request, 'searchstock.html', {'stocks': stocks, 'query': query})