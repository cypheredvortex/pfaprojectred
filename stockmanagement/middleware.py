from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Vous devez être connecté.")

            # Check if user has profile and role
            if not hasattr(request.user, 'profile'):
                return HttpResponseForbidden("Aucun rôle attribué.")

            user_role = request.user.profile.role
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Accès refusé.")
        return _wrapped_view
    return decorator