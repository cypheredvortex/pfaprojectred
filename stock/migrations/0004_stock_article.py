# Generated by Django 5.2 on 2025-04-17 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_article_fournisseur'),
        ('stock', '0003_remove_stock_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.article'),
        ),
    ]
