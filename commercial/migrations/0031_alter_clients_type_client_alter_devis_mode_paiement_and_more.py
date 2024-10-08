# Generated by Django 5.0.7 on 2024-08-19 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0030_mouvements_produit_qty_alter_devis_mode_paiement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='type_client',
            field=models.CharField(blank=True, choices=[('ent', 'Entreprise'), ('par', 'Particulier')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('esp', 'Espéce'), ('vir', 'Virement Bancaire'), ('chq', 'Chéque')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='devise',
            field=models.CharField(blank=True, choices=[('AFG', 'Afghanistan'), ('AGO', 'Angola'), ('ALB', 'Albanie'), ('ATG', 'Antigua-et-Barbuda'), ('ZAF', 'Afrique du Sud'), ('SAU', 'Arabie Saoudite'), ('DEU', 'Allemagne'), ('DZA', 'Algérie'), ('AND', 'Andorre')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='mouvements_produit',
            name='type_mouvement',
            field=models.CharField(blank=True, choices=[('ent', 'Entrée'), ('sor', 'Sortie')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='prospects',
            name='type_prospect',
            field=models.CharField(blank=True, choices=[('ent', 'Entreprise'), ('par', 'Particulier')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='etat',
            field=models.CharField(blank=True, choices=[('enc', 'En cours'), ('ann', 'Annuler'), ('att', 'En attente'), ('fin', 'Terminer')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='priority',
            field=models.CharField(blank=True, choices=[('me', 'Medium'), ('lo', 'Basse'), ('he', 'Haute')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='type_rappel',
            field=models.CharField(blank=True, choices=[('mes', 'Message'), ('tel', 'Appel téléphonique'), ('ema', 'Email')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produit', to='commercial.products'),
        ),
    ]
