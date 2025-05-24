"""
URL configuration for stockmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from pages.views import home_view
from pages.views import article_view
from pages.views import loginpage_view
from pages.views import stock_view
from pages.views import fournisseur_view
from pages.views import commands_view
from pages.views import rapport_view
from pages.views import gestionnaire_view
from pages.views import employe_view
from pages.views import listarticles_view
from pages.views import listcommands_view
from stock.views import get_stocks
from stock.views import create_stock
from stock.views import delete_stock
from stock.views import update_stock
from pages.views import update_stock_view
from article.views import get_articles
from article.views import create_article
from article.views import update_article
from pages.views import update_article_view
from article.views import delete_article
from commande.views import get_commands
from rapport.views import get_rapports
from rapport.views import create_rapport
from rapport.views import delete_rapport
from rapport.views import update_rapport
from pages.views import update_rapport_view
from .views import logout_view
from stock.views import list_stocks
from stock.views import liststocks_view
from article.views import list_articles
from pages.views import historique_view
from stock.views import get_stock_form
# from pages.views import get_stock_form_view
from rapport.views import get_rapport_form
from article.views import search_articles
from article.views import search_articles
from stock.views import search_stocks
from pages.views import get_dashboard
from rapport.views import rapport_pdf
from historiqueActions.views import gethistorique_view


import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('',home_view,name='home_view'),
    path('articlesview',article_view,name='article_view'),
    path('loginpage/',loginpage_view,name='loginpage_view'),
    path('stockview',stock_view,name='stock_view'),
    path('fournisseurs',fournisseur_view,name='fournisseurs_view'),
    path('commands',commands_view,name='commands_view'),
    path('rapportsview',rapport_view,name='rapport_view'),
    path('rapports/', get_rapports, name='get_rapports'),
    path('rapportmodify/', get_rapport_form, name='get_rapport_form'),
    path('createrapport', create_rapport, name='create_rapport'),
    path('deleterapport/<int:rapport_id>/', delete_rapport, name='delete_rapport'),
    path('updaterapport/<int:rapport_id>/', update_rapport, name='update_rapport'),
    path('updaterapportview/<int:rapport_id>/', update_rapport_view, name='update_rapport_view'),
    path('gestionnaire',gestionnaire_view,name='gestionnaire_view'),
    path('auth',views.auth_view,name='auth_view'),
    path('employe',employe_view,name='employe_view'),
    path('listarticlesview',listarticles_view,name='listarticles_view'),
    path('listcommandsview',listcommands_view,name='listcommands_view'),
    path('liststocksview',liststocks_view,name='liststocks_view'),
    path('liststocks', list_stocks, name='list_stocks'),
    path('stocks/', get_stocks, name='get_stocks'),
    path('stockmodify/', get_stock_form, name='get_stock_form'),
    # path('stockmodifyview',get_stock_form_view,name='stockmodifyview'),
    path('createstock', create_stock, name='create_stock'),
    path('deletestock/<int:stock_id>/', delete_stock, name='delete_stock'),
    path('updatestockview/<int:stock_id>/', update_stock_view, name='update_stock_view'),  # Update (View)
    path('updatestock/<int:stock_id>/', update_stock, name='update_stock'),
    path('listarticles',list_articles,name='list_articles'),
    path('articles/', get_articles, name='get_articles'),
    path('createarticle/', create_article, name='create_article'),  # Create
    path('updatearticleview/<int:article_id>/', update_article_view, name='update_article_view'),  # Update (View)
    path('updatearticle/<int:article_id>/', update_article, name='update_article'),  # Update (Action)
    path('deletearticle/<int:article_id>/', delete_article, name='delete_article'),  # Delete
    path('listcommands',get_commands,name='get_commands'),
    path('logout/', logout_view, name='logout_view'),
    path('historique',historique_view,name='historique_view'),
    path('gethistorique',gethistorique_view,name='gethistorique_view'),
    path('searcharticles', search_articles, name='search_articles'),
    path('searchstock', search_stocks, name='search_stocks'),
    path('getdashboard', get_dashboard, name='get_dashboard'),
    path('dashboard',views.dashboard_view,name='dashboard_view'),
    path('api/metrics/turnover-rate/', views.calculate_turnover_rate, name='turnover_rate'),
    path('api/metrics/restock-time/', views.calculate_avg_restock_time, name='restock_time'),
    path('api/metrics/inventory-accuracy/', views.calculate_inventory_accuracy, name='inventory_accuracy'),
    path('api/metrics/monthly-growth/', views.calculate_monthly_growth, name='monthly_growth'),
    path('rapport/pdf/', rapport_pdf, name='rapport_pdf'),
    
    ]