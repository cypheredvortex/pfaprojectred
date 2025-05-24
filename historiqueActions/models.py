from django.db import models
from django.contrib.auth.models import User

class HistoriqueActions(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.utilisateur.username} - {self.action} - {self.date_action}"