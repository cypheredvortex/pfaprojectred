from django.db import models
from datetime import date

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    references = models.CharField(max_length=50, null=True, blank=True)
    categorie = models.CharField(max_length=50, null=True, blank=True)
    prix = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantite = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)  # Description détaillée de l'article
    date_ajout = models.DateField(default=date.today)

    class Etat(models.TextChoices):
        EN_STOCK = "en_stock", "En stock"
        HORS_STOCK = "hors_stock", "Hors stock"

    etat = models.CharField(max_length=15, choices=Etat.choices, default=Etat.HORS_STOCK)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):    
        super().save(*args, **kwargs)
        if self.quantite < 10:
            print('Stock faible')
        elif self.quantite == 0:
            print('Stock vide')
        elif self.quantite > 100:
            print('Stock suffisant')
        elif 50 < self.quantite <= 100:
            print('Stock moyen')