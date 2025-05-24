from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import UserProfile  # Make sure this matches your app name
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, F, Count
from article.models import Article
from stock.models import Stock
from commande.models import Commande, ArticleCommande
from datetime import timedelta
from django.utils import timezone
import datetime
from collections import defaultdict
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import datetime, timedelta, date
import json
from article.models import Article
from stock.models import Stock
from commande.models import Commande, ArticleCommande
from fournisseur.models import FournisseurArticle
from rapport.models import Rapport
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.functions import TruncMonth





def auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            try:
                user_profile = user.profile  # because of related_name='profile'
                role = user_profile.role

                if user.is_superuser or role == UserProfile.Roles.ADMIN:
                    return redirect('/admin/')
                elif role == UserProfile.Roles.EMPLOYE:
                    return redirect('list_stocks')
                elif role == UserProfile.Roles.STOCK_MANAGER:
                    return redirect('get_stocks')
                else:
                    messages.error(request, "Unknown role.")
                    return redirect('loginpage_view')

            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('loginpage_view')
                
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('loginpage_view')

    return render(request, 'loginpage.html')

  # Redirects to login page if user isn't authenticated
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('loginpage_view')


from django.db.models import Sum, F, Count, Avg, Q,Case,When,Value,ExpressionWrapper,FloatField
from django.db.models.functions import Cast
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from datetime import date, timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder
from historiqueActions.models import HistoriqueActions
from article.models import Article
from fournisseur.models import Fournisseur
from commande.models import ArticleCommande, Commande
from stock.models import Stock
from rapport.models import Rapport
from fournisseur.models import FournisseurArticle

@login_required
def dashboard_view(request):
    # Basic Statistics
    total_articles = Article.objects.count()
    total_stock = Stock.objects.aggregate(Sum('quantiteDisponible'))['quantiteDisponible__sum'] or 0
    low_stock_threshold = 10
    low_stock_articles = Article.objects.filter(quantite__lt=low_stock_threshold)
    
    # Time-based metrics
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    
    # Stock movements
    stock_entries = Stock.objects.filter(
        type="entree", 
        date__gte=thirty_days_ago
    ).aggregate(
        count=Count('id'),
        total_quantity=Sum('quantiteDisponible')
    )
    
    stock_exits = Stock.objects.filter(
        type="sortie", 
        date__gte=thirty_days_ago
    ).aggregate(
        count=Count('id'),
        total_quantity=Sum('quantiteDisponible')
    )
    
    # Stock trends by day
    stock_trends = Stock.objects.filter(
        date__gte=thirty_days_ago
    ).values('date').annotate(
        entries=Sum('quantiteDisponible', filter=Q(type='entree')),
        exits=Sum('quantiteDisponible', filter=Q(type='sortie'))
    ).order_by('date')
    
    # Article performance
    top_articles = ArticleCommande.objects.values(
        'article__nom', 
        'article__categorie'
    ).annotate(
        total_quantity=Sum('quantite'),
        total_revenue=Sum(F('quantite') * F('prix_unitaire'))
    ).order_by('-total_quantity')[:10]
    
    # Category analysis
    category_stats = Article.objects.values('categorie').annotate(
        total_articles=Count('id'),
        total_stock=Sum('quantite'),
        avg_price=Avg('prix')
    )
    
    # User activity
    user_activity = HistoriqueActions.objects.filter(
        date_action__gte=thirty_days_ago
    ).values('utilisateur__username').annotate(
        action_count=Count('id')
    ).order_by('-action_count')[:5]
    
    # Financial metrics
    financial_metrics = {
        'total_revenue': Commande.objects.filter(
            dateCommande__gte=thirty_days_ago,
            etatCommande='complete'
        ).aggregate(total=Sum('prix'))['total'] or 0,
        'avg_order_value': Commande.objects.filter(
            dateCommande__gte=thirty_days_ago,
            etatCommande='complete'
        ).aggregate(avg=Avg('prix'))['avg'] or 0
    }

    # Enhanced Stock Metrics
    stock_metrics = {
        'turnover_rate': calculate_turnover_rate(),
        'out_of_stock_count': Article.objects.filter(quantite=0).count(),
        'avg_restock_time': calculate_avg_restock_time(),
        'total_value': Article.objects.aggregate(
            total=Sum(F('quantite') * F('prix')))['total'] or 0
    }
    
    # Performance Metrics
    total_orders = Commande.objects.filter(
        dateCommande__gte=thirty_days_ago
    ).count()
    
    completed_orders = Commande.objects.filter(
        dateCommande__gte=thirty_days_ago,
        etatCommande='complete'
    ).count()
    
    performance_metrics = {
        'fulfillment_rate': (completed_orders / total_orders * 100) if total_orders > 0 else 0,
        'inventory_accuracy': calculate_inventory_accuracy(),
        'monthly_growth': calculate_monthly_growth(),
        'active_skus': Article.objects.filter(quantite__gt=0).count()
    }
    
    # Category Distribution
    category_distribution = Article.objects.values('categorie').annotate(
        count=Count('id'),
        category=F('categorie')
    ).order_by('-count')

    # Supplier Performance
    supplier_performance = Commande.objects.values(
        'fournisseur__nom'
    ).annotate(
        total_orders=Count('id'),
        completed_orders=Count('id', filter=Q(etatCommande='complete')),
        on_time_rate=ExpressionWrapper(
            Cast(Count('id', filter=Q(etatCommande='complete')) * 100.0 / 
                Case(When(total_orders=0, then=Value(1)), default='total_orders'),
                output_field=FloatField()),
            output_field=FloatField()
        )
    ).order_by('-total_orders')[:5]
    
    context = {
        
        'total_articles': total_articles,
        'total_stock': total_stock,
        'low_stock_articles': low_stock_articles,
        'stock_entries': stock_entries,
        'stock_exits': stock_exits,
        'stock_trends': json.dumps(list(stock_trends), cls=DjangoJSONEncoder),
        'top_articles': json.dumps(list(top_articles), cls=DjangoJSONEncoder),
        'category_stats': category_stats,
        'user_activity': user_activity,
        'financial_metrics': financial_metrics,
        'date_range': {
            'start': thirty_days_ago,
            'end': today
        }
        
    }
    context.update({
        'stock_metrics': stock_metrics,
        'performance_metrics': performance_metrics,
        'category_distribution': json.dumps(list(category_distribution), cls=DjangoJSONEncoder)
    })
    # Supplier Performance
    supplier_performance = Commande.objects.values(
        'fournisseur__nom'
    ).annotate(
        total_orders=Count('id'),
        completed_orders=Count('id', filter=Q(etatCommande='complete')),
        on_time_rate=ExpressionWrapper(
            Cast(Count('id', filter=Q(etatCommande='complete')) * 100.0 / 
                Case(When(total_orders=0, then=Value(1)), default='total_orders'),
                output_field=FloatField()),
            output_field=FloatField()
        )
    ).order_by('-total_orders')[:5]
    
    context.update({
        'supplier_performance': json.dumps(list(supplier_performance), cls=DjangoJSONEncoder)
    })
    
    return render(request, 'dashboard.html', context)

def calculate_turnover_rate():
    """Calculate inventory turnover rate for the last 30 days"""
    thirty_days_ago = date.today() - timedelta(days=30)
    total_stock_value = Article.objects.aggregate(
        total=Sum(F('quantite') * F('prix')))['total'] or 1  # Avoid division by zero
    
    total_sales = ArticleCommande.objects.filter(
        commande__dateCommande__gte=thirty_days_ago
    ).aggregate(
        total=Sum(F('quantite') * F('prix_unitaire')))['total'] or 0
    
    return (total_sales / total_stock_value) * 100

def calculate_avg_restock_time():
    """Calculate average time between stock entries"""
    thirty_days_ago = date.today() - timedelta(days=30)
    stock_entries = Stock.objects.filter(
        type='entree',
        date__gte=thirty_days_ago
    ).order_by('date')
    
    if stock_entries.count() < 2:
        return 0
    
    total_days = 0
    entries_count = stock_entries.count() - 1
    previous_date = None
    
    for entry in stock_entries:
        if previous_date:
            total_days += (entry.date - previous_date).days
        previous_date = entry.date
    
    return round(total_days / entries_count) if entries_count > 0 else 0

def calculate_inventory_accuracy():
    """Calculate inventory accuracy based on physical vs system counts"""
    # This is a placeholder - in real world, you'd compare physical inventory counts
    # with system counts. Here we're assuming 95% accuracy
    return 95

def calculate_monthly_growth():
    """Calculate monthly growth rate in stock value"""
    current_month = date.today().replace(day=1)
    previous_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_value = Stock.objects.filter(
        date__gte=current_month
    ).aggregate(
        total=Sum('quantiteDisponible'))['total'] or 0
    
    previous_value = Stock.objects.filter(
        date__gte=previous_month,
        date__lt=current_month
    ).aggregate(
        total=Sum('quantiteDisponible'))['total'] or 1  # Avoid division by zero
    
    growth_rate = ((current_value - previous_value) / previous_value) * 100
    return round(growth_rate, 2)
