# Generated by Django 5.1.7 on 2025-04-12 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0001_initial'),
        ('fournisseur', '0002_alter_fournisseur_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='fournisseurId',
        ),
        migrations.AddField(
            model_name='commande',
            name='fournisseur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fournisseur.fournisseur'),
        ),
    ]
