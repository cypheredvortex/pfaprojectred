from django.db import models
from article.models import Article
from django.contrib.auth.models import User

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True, blank=True)

    class TypeChoices(models.TextChoices):
        ENTREE = "entree", "Entrée"
        SORTIE = "sortie", "Sortie"

    class EtatChoices(models.TextChoices):
        EN_ALERTE = "en_alerte", "En alerte"
        HORS_ALERTE = "hors_alerte", "Hors alerte"

    type = models.CharField(max_length=10, choices=TypeChoices.choices, default=TypeChoices.ENTREE)
    etatStock = models.CharField(max_length=15, choices=EtatChoices.choices, default=EtatChoices.HORS_ALERTE)
    quantiteDisponible = models.IntegerField()
    seuilAlerte = models.IntegerField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Ajout de l'utilisateur qui effectue le mouvement

    def __str__(self):
        return f"Stock pour {self.article.nom} (ID: {self.id})"