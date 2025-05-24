from django.urls import path
from . import views
from pages.views import article_view

urlpatterns = [
    path('articles',article_view, name='article_view'),
]