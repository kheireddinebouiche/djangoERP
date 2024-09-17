# Generated by Django 5.0.7 on 2024-07-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0005_alter_notes_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prospects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('prenom', models.CharField(blank=True, max_length=100, null=True)),
                ('type_prospect', models.CharField(blank=True, choices=[('Particulier', 'Particulier'), ('Entreprise', 'Entreprise')], max_length=100, null=True)),
            ],
        ),
    ]
