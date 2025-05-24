from django.db import models
from fournisseur.models import Fournisseur
from article.models import Article

class Commande(models.Model):
    id = models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    dateCommande = models.DateField()
    etatCommande = models.CharField(
        max_length=15,
        choices=[("en_cours", "En cours"), ("complete", "Complete"), ("annule", "Annulé")],
        default="en_cours"
    )
    prix = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return f"Commande {self.id} - Fournisseur: {self.fournisseur.nom}"

class ArticleCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Article: {self.article.nom} - Quantité: {self.quantite}"