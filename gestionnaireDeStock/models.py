from django.db import models
from django.conf import settings 
# Create your models here.
class GestionnaireDeStock(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, null=True, blank=True) 