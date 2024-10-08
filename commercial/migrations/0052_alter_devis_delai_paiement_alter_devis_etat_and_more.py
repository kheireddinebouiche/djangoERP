# Generated by Django 5.0.7 on 2024-08-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0051_alter_ligne_facture_options_ligne_facture_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devis',
            name='delai_paiement',
            field=models.CharField(blank=True, choices=[('30j', 'A 30 jours'), ('rec', 'A réception'), ('imm', 'Immédiat')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='etat',
            field=models.CharField(blank=True, choices=[('fac', 'A facturé'), ('ter', 'Terminer'), ('ann', 'Annulé'), ('bro', 'Brouillon')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='delai_paiement',
            field=models.CharField(blank=True, choices=[('30j', 'A 30 jours'), ('rec', 'A réception'), ('imm', 'Immédiat')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='etat',
            field=models.CharField(blank=True, choices=[('fac', 'A facturé'), ('ter', 'Terminer'), ('ann', 'Annulé'), ('bro', 'Brouillon')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='devise',
            field=models.CharField(blank=True, choices=[('DZA', 'Algérie'), ('AND', 'Andorre'), ('SAU', 'Arabie Saoudite'), ('ZAF', 'Afrique du Sud'), ('AGO', 'Angola'), ('DEU', 'Allemagne'), ('AFG', 'Afghanistan'), ('ALB', 'Albanie'), ('ATG', 'Antigua-et-Barbuda')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='type_profile',
            field=models.CharField(blank=True, choices=[('ven', 'Vendeurs'), ('adm', 'Administrateur')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='etat',
            field=models.CharField(blank=True, choices=[('fin', 'Terminer'), ('enc', 'En cours'), ('att', 'En attente'), ('ann', 'Annuler')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='priority',
            field=models.CharField(blank=True, choices=[('he', 'Haute'), ('lo', 'Basse'), ('me', 'Medium')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='type_rappel',
            field=models.CharField(blank=True, choices=[('mes', 'Message'), ('tel', 'Appel téléphonique'), ('ema', 'Email')], max_length=3, null=True),
        ),
    ]
