from django.shortcuts import render, redirect
from django.http import JsonResponse
from commande.models import Commande
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from user.models import UserProfile
from stockmanagement.middleware import role_required  
# Helper to disable cache
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
@role_required(['employe'])  # Use the decorator correctly
def get_commands(request):
    if not request.user.is_authenticated or not user.is_employe:
        return redirect('/loginpage/')
    
    commands = Commande.objects.all()
    response = render(request, 'listcommands.html', {'commands': commands})
    return disable_cache(response)