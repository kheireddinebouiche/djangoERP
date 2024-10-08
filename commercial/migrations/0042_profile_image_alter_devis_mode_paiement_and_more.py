# Generated by Django 5.0.7 on 2024-08-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0041_profile_date_recrutement_profile_etat_profile_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_image/'),
        ),
        migrations.AlterField(
            model_name='devis',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('chq', 'Chéque'), ('esp', 'Espéce'), ('vir', 'Virement Bancaire')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='generalsettings',
            name='devise',
            field=models.CharField(blank=True, choices=[('ATG', 'Antigua-et-Barbuda'), ('AGO', 'Angola'), ('ALB', 'Albanie'), ('ZAF', 'Afrique du Sud'), ('SAU', 'Arabie Saoudite'), ('AFG', 'Afghanistan'), ('DEU', 'Allemagne'), ('DZA', 'Algérie'), ('AND', 'Andorre')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='type_profile',
            field=models.CharField(blank=True, choices=[('adm', 'Administrateur'), ('ven', 'Vendeurs')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='etat',
            field=models.CharField(blank=True, choices=[('att', 'En attente'), ('ann', 'Annuler'), ('fin', 'Terminer'), ('enc', 'En cours')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rappels',
            name='type_rappel',
            field=models.CharField(blank=True, choices=[('ema', 'Email'), ('tel', 'Appel téléphonique'), ('mes', 'Message')], max_length=3, null=True),
        ),
    ]
