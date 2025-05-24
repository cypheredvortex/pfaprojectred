from django.db import models
from django.contrib.auth.models import User

class Rapport(models.Model):
    id = models.AutoField(primary_key=True)
    stock=models.ForeignKey('stock.Stock', on_delete=models.CASCADE,default=None,null=True)
    # stockId = models.IntegerField()
    dateRapport = models.DateField()
    # mouvementDeStock = models.CharField(max_length=20)
    # etatStock = models.CharField(max_length=20)
    
    vente = models.CharField(max_length=20)
    approvisionnement = models.CharField(max_length=20)
    type_rapport = models.CharField(max_length=20,default="journalier",choices=[('mensuel', 'Mensuel'), ('hebdomadaire', 'Hebdomadaire'), ('journalier', 'Journalier'),])
    contenu = models.TextField(default="")  # Contenu du rapport
    généré_par = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f"Rapport {self.id} - {self.dateRapport}"