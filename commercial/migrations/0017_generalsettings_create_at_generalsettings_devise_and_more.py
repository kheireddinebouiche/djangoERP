# Generated by Django 5.0.7 on 2024-08-18 13:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0016_alter_devis_mode_paiement_alter_rappels_etat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsettings',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generalsettings',
            name='devise',
            field=models.CharField(blank=True, choices=[('AND', 'Andorre'), ('AFG', 'Afghanistan'), ('ATG', 'Antigua-et-Barbuda'), ('ZAF', 'Afrique du Sud'), ('SAU', 'Arabie Saoudite'), ('ALB', 'Albanie'), ('DZA', 'Algérie'), ('DEU', 'Allemagne'), ('AGO', 'Angola')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='generalsettings',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('vir', 'Virement Bancaire'), ('chq', 'Chéque'), ('esp', 'Espéce')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='type_rappel',
            field=models.CharField(blank=True, choices=[('ema', 'Email'), ('tel', 'Appel téléphonique'), ('mes', 'Message')], max_length=3, null=True),
        ),
    ]
