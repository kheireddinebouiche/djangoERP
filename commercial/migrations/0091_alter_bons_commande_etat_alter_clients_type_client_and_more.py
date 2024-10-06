# Generated by Django 4.2.16 on 2024-10-06 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0090_retourproduit_qty_alter_bons_commande_etat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bons_commande',
            name='etat',
            field=models.CharField(blank=True, choices=[('ann', 'Annuler'), ('val', 'Valider'), ('bro', 'Brouillon')], default='bro', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='type_client',
            field=models.CharField(blank=True, choices=[('par', 'Particulier'), ('ent', 'Entreprise')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='etat',
            field=models.CharField(blank=True, choices=[('ann', 'Annulé'), ('ter', 'Terminer'), ('fac', 'A facturé'), ('bro', 'Brouillon')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('chq', 'Chéque'), ('vir', 'Virement Bancaire'), ('esp', 'Espéce')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='etat',
            field=models.CharField(blank=True, choices=[('ter', 'Terminer'), ('val', 'Valider'), ('bro', 'Brouillon')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('chq', 'Chéque'), ('vir', 'Virement Bancaire'), ('esp', 'Espéce')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='facture_avoir',
            name='etat',
            field=models.CharField(blank=True, choices=[('ter', 'Terminer'), ('bro', 'Brouillon')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='devise',
            field=models.CharField(blank=True, choices=[('ATG', 'Antigua-et-Barbuda'), ('ZAF', 'Afrique du Sud'), ('ALB', 'Albanie'), ('DEU', 'Allemagne'), ('AND', 'Andorre'), ('AGO', 'Angola'), ('DZA', 'Algérie'), ('SAU', 'Arabie Saoudite'), ('AFG', 'Afghanistan')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='mouvements_produit',
            name='type_mouvement',
            field=models.CharField(blank=True, choices=[('ent', 'Entrée'), ('sor', 'Sortie')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='paiementclient',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('chq', 'Chéque'), ('vir', 'Virement Bancaire'), ('esp', 'Espéce')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='type_produit',
            field=models.CharField(blank=True, choices=[('srv', 'Service'), ('pro', 'Produit')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='type_tarifcation',
            field=models.CharField(blank=True, choices=[('a', 'Année'), ('j', 'Jour'), ('m', 'Mois'), ('h', 'Horaire')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='prospects',
            name='type_prospect',
            field=models.CharField(blank=True, choices=[('par', 'Particulier'), ('ent', 'Entreprise')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='etat',
            field=models.CharField(blank=True, choices=[('fin', 'Terminer'), ('enc', 'En cours'), ('att', 'En attente'), ('ann', 'Annuler')], max_length=3, null=True),
        ),
        migrations.CreateModel(
            name='PaiementsFournisseurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('ref_paiement', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ref_bon_commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commercial.bons_commande')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Paiement du fournisseur',
                'verbose_name_plural': 'Paiements des fournisseurs',
            },
        ),
    ]
