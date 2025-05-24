from django.db import models
from article.models import Article

class Fournisseur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    adresse = models.CharField(max_length=200)
    numero_tva = models.CharField(max_length=20, null=True, blank=True)  # Numéro de TVA
    conditions_paiement = models.TextField(null=True, blank=True)  # Conditions de paiement

    def __str__(self):
        return self.nom

class FournisseurArticle(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    prix_achat = models.DecimalField(decimal_places=2, max_digits=10)  # Prix d'achat

    def __str__(self):
        return f"{self.fournisseur.nom} - {self.article.nom}"