from django.shortcuts import render, get_object_or_404, redirect
from .models import Rapport
from stock.models import Stock
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.apps import apps
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from user.models import UserProfile


# Helper to disable caching
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
def create_rapport(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock')
        date_rapport = request.POST.get('dateRapport')
        vente = request.POST.get('vente')
        approvisionnement = request.POST.get('approvisionnement')
        type_rapport = request.POST.get('type_rapport')
        contenu = request.POST.get('contenu')

        try:
            stock = get_object_or_404(Stock, id=int(stock_id))
            date_rapport = datetime.strptime(date_rapport, '%Y-%m-%d').date()

            Rapport.objects.create(
                stock=stock,
                dateRapport=date_rapport,
                vente=vente,
                approvisionnement=approvisionnement,
                type_rapport=type_rapport,
                contenu=contenu,
                généré_par=request.user
            )
            return redirect('get_rapports')

        except (ValueError, TypeError, Stock.DoesNotExist) as e:
            return render(request, 'rapport_form.html', {
                'error': f"Erreur lors de la soumission : {e}",
                'stocks': Stock.objects.all()
            })

    response=render(request, 'rapport_form.html', {
        'stocks': Stock.objects.all()
    })
    disable_cache(response)


@never_cache
@login_required(login_url='/loginpage/')
def get_rapports(request):
    rapports = Rapport.objects.all()
    response = render(request, 'rapports.html', {'rapports': rapports})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        rapport.stock_id = request.POST.get('stock')
        rapport.dateRapport = request.POST.get('dateRapport')
        rapport.vente = request.POST.get('vente')
        rapport.approvisionnement = request.POST.get('approvisionnement')
        rapport.type_rapport = request.POST.get('type_rapport')
        rapport.contenu = request.POST.get('contenu')
        rapport.save()
        return redirect('get_rapports')

    stocks = Stock.objects.all()
    response = render(request, 'rapport_form.html', {
        'rapport': rapport,
        'stocks': stocks
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def delete_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        rapport.delete()
        return redirect('get_rapports')

    response = render(request, 'rapport_confirm_delete.html', {'rapport': rapport})
    return disable_cache(response)


@never_cache
@login_required(login_url='/loginpage/')
def get_rapport_form(request):
    # Retrieve the Rapport and Stock models dynamically
    Rapport = apps.get_model('rapport', 'Rapport')
    Stock = apps.get_model('stock', 'Stock')

    rapports = Rapport.objects.all()
    stocks = Stock.objects.all()

    response = render(request, 'rapport_form.html', {  # Render the form to add/edit a report
        'rapports': rapports,
        'stocks': stocks,
    })
    return disable_cache(response)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF')
    return response


def rapport_pdf(request):
    context = {'nom': 'Yasser', 'produits': ['Article A', 'Article B']}
    return render_to_pdf('rapport_template.html', context)

def rapport_pdf(request):
    rapports = Rapport.objects.all()
    template = get_template('rapport_pdf.html')
    html = template.render({'rapports': rapports})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_stock.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response