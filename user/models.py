from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STOCK_MANAGER = 'stock_manager', 'Stock Manager'
        EMPLOYE = 'employe', 'Employé'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.EMPLOYE)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"