# Generated by Django 5.0.7 on 2024-08-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0035_remove_lignecaisse_caisse_alter_clients_type_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devis',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('esp', 'Espéce'), ('chq', 'Chéque'), ('vir', 'Virement Bancaire')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='devise',
            field=models.CharField(blank=True, choices=[('DZA', 'Algérie'), ('ZAF', 'Afrique du Sud'), ('AGO', 'Angola'), ('AFG', 'Afghanistan'), ('DEU', 'Allemagne'), ('AND', 'Andorre'), ('ATG', 'Antigua-et-Barbuda'), ('SAU', 'Arabie Saoudite'), ('ALB', 'Albanie')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='etat',
            field=models.CharField(blank=True, choices=[('enc', 'En cours'), ('fin', 'Terminer'), ('ann', 'Annuler'), ('att', 'En attente')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='priority',
            field=models.CharField(blank=True, choices=[('lo', 'Basse'), ('he', 'Haute'), ('me', 'Medium')], max_length=2, null=True),
        ),
    ]
