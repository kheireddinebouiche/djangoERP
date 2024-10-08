# Generated by Django 5.0.7 on 2024-09-19 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commercial", "0084_bons_commande_etat_alter_devis_delai_paiement_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bons_commande",
            name="etat",
            field=models.CharField(
                blank=True,
                choices=[("bro", "Brouillon"), ("ann", "Annuler"), ("val", "Valider")],
                default="bro",
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="clients",
            name="type_client",
            field=models.CharField(
                blank=True,
                choices=[("ent", "Entreprise"), ("par", "Particulier")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="devis",
            name="etat",
            field=models.CharField(
                blank=True,
                choices=[
                    ("bro", "Brouillon"),
                    ("fac", "A facturé"),
                    ("ter", "Terminer"),
                    ("ann", "Annulé"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="devis",
            name="mode_paiement",
            field=models.CharField(
                blank=True,
                choices=[
                    ("chq", "Chéque"),
                    ("vir", "Virement Bancaire"),
                    ("esp", "Espéce"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="facture",
            name="etat",
            field=models.CharField(
                blank=True,
                choices=[("bro", "Brouillon"), ("ter", "Terminer")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="facture",
            name="mode_paiement",
            field=models.CharField(
                blank=True,
                choices=[
                    ("chq", "Chéque"),
                    ("vir", "Virement Bancaire"),
                    ("esp", "Espéce"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="facture_avoir",
            name="etat",
            field=models.CharField(
                blank=True,
                choices=[("bro", "Brouillon"), ("ter", "Terminer")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="generalsettings",
            name="devise",
            field=models.CharField(
                blank=True,
                choices=[
                    ("AND", "Andorre"),
                    ("SAU", "Arabie Saoudite"),
                    ("ALB", "Albanie"),
                    ("DEU", "Allemagne"),
                    ("ZAF", "Afrique du Sud"),
                    ("AGO", "Angola"),
                    ("DZA", "Algérie"),
                    ("ATG", "Antigua-et-Barbuda"),
                    ("AFG", "Afghanistan"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="mouvements_produit",
            name="type_mouvement",
            field=models.CharField(
                blank=True,
                choices=[("ent", "Entrée"), ("sor", "Sortie")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="paiementclient",
            name="mode_paiement",
            field=models.CharField(
                blank=True,
                choices=[
                    ("chq", "Chéque"),
                    ("vir", "Virement Bancaire"),
                    ("esp", "Espéce"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="products",
            name="type_produit",
            field=models.CharField(
                blank=True,
                choices=[("srv", "Service"), ("pro", "Produit")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="products",
            name="type_tarifcation",
            field=models.CharField(
                blank=True,
                choices=[
                    ("m", "Mois"),
                    ("j", "Jour"),
                    ("a", "Année"),
                    ("h", "Horaire"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="type_profile",
            field=models.CharField(
                blank=True,
                choices=[("ven", "Vendeurs"), ("adm", "Administrateur")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="prospects",
            name="type_prospect",
            field=models.CharField(
                blank=True,
                choices=[("ent", "Entreprise"), ("par", "Particulier")],
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="rappels",
            name="etat",
            field=models.CharField(
                blank=True,
                choices=[
                    ("enc", "En cours"),
                    ("ann", "Annuler"),
                    ("att", "En attente"),
                    ("fin", "Terminer"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="rappels",
            name="priority",
            field=models.CharField(
                blank=True,
                choices=[("lo", "Basse"), ("me", "Medium"), ("he", "Haute")],
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="rappels",
            name="type_rappel",
            field=models.CharField(
                blank=True,
                choices=[
                    ("tel", "Appel téléphonique"),
                    ("mes", "Message"),
                    ("ema", "Email"),
                ],
                max_length=3,
                null=True,
            ),
        ),
    ]
