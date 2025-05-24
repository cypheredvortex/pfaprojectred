from django.shortcuts import render
from django.db.models import Sum
from commande.models import Commande, ArticleCommande
from article.models import Article
from stock.models import Stock
from fournisseur.models import FournisseurArticle
from datetime import timedelta
from django.utils import timezone
from datetime import datetime, timedelta, date
import json

from datetime import date, timedelta
from django.db.models import Sum, F, Min, Max, Avg
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def gethistorique_view(request):
    today = date.today()
    first_day_of_this_month = today.replace(day=1)
    first_day_of_last_month = (first_day_of_this_month - timedelta(days=1)).replace(day=1)

    total_revenue = Commande.objects.filter(etatCommande='complete').aggregate(Sum('prix'))['prix__sum'] or 0
    total_orders = Commande.objects.count()
    average_order_value = total_revenue / total_orders if total_orders else 0
    total_stock_qty = Article.objects.aggregate(Sum('quantite'))['quantite__sum'] or 0

    current_month_revenue = Commande.objects.filter(
        dateCommande__gte=first_day_of_this_month,
        etatCommande='complete'
    ).aggregate(Sum('prix'))['prix__sum'] or 0

    last_month_revenue = Commande.objects.filter(
        dateCommande__gte=first_day_of_last_month,
        dateCommande__lt=first_day_of_this_month,
        etatCommande='complete'
    ).aggregate(Sum('prix'))['prix__sum'] or 0

    sales_growth = ((current_month_revenue - last_month_revenue) / last_month_revenue * 100) if last_month_revenue else 0

    revenue_qs = (
        Commande.objects.filter(etatCommande='complete')
        .annotate(month=TruncMonth('dateCommande'))
        .values('month')
        .annotate(total=Sum('prix'))
        .order_by('month')
    )
    revenue_data = [{"date": r["month"].strftime("%Y-%m"), "revenue": r["total"]} for r in revenue_qs]
    revenue_labels = [r["date"] for r in revenue_data]
    revenue_values = [r["revenue"] for r in revenue_data]

    stock_entries_qs = (
        Stock.objects.filter(type='entree')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(movement=Sum('quantiteDisponible'))
        .order_by('month')
    )

    stock_exits_qs = (
        Stock.objects.filter(type='sortie')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(movement=Sum('quantiteDisponible'))
        .order_by('month')
    )

    stock_entries_data = [{"date": s["month"].strftime("%Y-%m"), "movement": s["movement"] or 0} for s in stock_entries_qs]
    stock_exits_data = [{"date": s["month"].strftime("%Y-%m"), "movement": s["movement"] or 0} for s in stock_exits_qs]

    stock_labels = list(set([s["date"] for s in stock_entries_data] + [s["date"] for s in stock_exits_data]))
    stock_labels.sort()

    stock_entries_values = [next((entry["movement"] for entry in stock_entries_data if entry["date"] == month), 0) for month in stock_labels]
    stock_exits_values = [next((exit["movement"] for exit in stock_exits_data if exit["date"] == month), 0) for month in stock_labels]

    article_qs = (
        ArticleCommande.objects.values('article__nom')
        .annotate(demand=Sum('quantite'))
        .order_by('-demand')[:10]
    )
    articles_data = [{"nom": a["article__nom"], "demand": a["demand"]} for a in article_qs]
    growth_potential_data = [{"article": a["article__nom"], "growth": a["demand"] * 0.1} for a in article_qs]

    total_purchase_cost = FournisseurArticle.objects.aggregate(total=Sum('prix_achat'))['total'] or 0
    profit = total_revenue - total_purchase_cost

    low_stock_articles = Article.objects.filter(quantite__lt=10)
    low_stock_value = low_stock_articles.aggregate(
        total=Sum(F('quantite') * F('prix'))
    )['total'] or 0

    sales_per_article = ArticleCommande.objects.values('article__nom').annotate(
        total_sales=Sum(F('quantite') * F('prix_unitaire'))
    ).order_by('-total_sales')

    supplier_spend = Commande.objects.values('fournisseur__nom').annotate(
        total_spend=Sum('prix')
    ).order_by('-total_spend')

    cost_per_article = FournisseurArticle.objects.values('article__nom').annotate(
        min_cost=Min('prix_achat'),
        max_cost=Max('prix_achat'),
        avg_cost=Avg('prix_achat')
    ).order_by('article__nom')

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'average_order_value': round(average_order_value, 2),
        'total_stock_qty': total_stock_qty,
        'sales_growth': round(sales_growth, 2),
        'revenue_data': revenue_data,
        'revenue_labels': json.dumps(revenue_labels, cls=DjangoJSONEncoder),
        'revenue_values': json.dumps(revenue_values, cls=DjangoJSONEncoder),
        'stock_movements_data': stock_entries_data + stock_exits_data,
        'stock_labels': json.dumps(stock_labels, cls=DjangoJSONEncoder),
        'stock_entries_values': json.dumps(stock_entries_values, cls=DjangoJSONEncoder),
        'stock_exits_values': json.dumps(stock_exits_values, cls=DjangoJSONEncoder),
        'articles_data': articles_data,
        'growth_potential_data': growth_potential_data,
        'total_purchase_cost': total_purchase_cost,
        'profit': round(profit, 2),
        'low_stock_value': low_stock_value,
        'sales_per_article': sales_per_article,
        'supplier_spend': supplier_spend,
        'cost_per_article': cost_per_article,
    }

    return render(request, 'historique.html', context)