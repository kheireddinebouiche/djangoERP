from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Profile)

admin.site.register(Contact)

@admin.register(Products)
class ProductsClass(admin.ModelAdmin):
    list_display = ('id','designation','ref','created_at')

@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    list_display = ('num','etat','created_at')

@admin.register(SessionVente)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('num', 'created_at','etat','caisse')  

admin.site.register(Tva)

@admin.register(LigneCaisse)
class LigneCaisseAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty','montant_total','session', 'created_at')

admin.site.register(Stock)

@admin.register(Mouvements_produit)
class LigneTypeMouvement(admin.ModelAdmin):
    list_display = ('id','produit','qty','type_mouvement','created_at')

admin.site.register(Clients)
admin.site.register(Fournisseurs)

@admin.register(Devis)
class DevisAdmin(admin.ModelAdmin):
    list_display = ('number', 'created_at', 'client')
    
@admin.register(Ligne_Devis)
class LigneDevisClass(admin.ModelAdmin):
    list_display = ('id','produit', 'qty', 'ht', 'tva', 'ttc')

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'client', 'etat')

@admin.register(Ligne_Facture)
class LigneFactureClass(admin.ModelAdmin):
    list_display = ('id','produit', 'qty', 'ht', 'tva', 'ttc')

@admin.register(Bons_livraison)
class BonsLivraisonClass(admin.ModelAdmin):
    list_display = ('id', 'number', 'client' )

@admin.register(Lignes_bon_livraison)
class LignesBonLivraisonClass(admin.ModelAdmin):
    list_display = ('id', 'user', 'bon_livraison','qty','total','created_at')

admin.site.register(RetourProduit)
admin.site.register(PaiementClient)
admin.site.register(Notes)
admin.site.register(Prospects)
admin.site.register(Rappels)
admin.site.register(GeneralSettings)
admin.site.register(Infos_Entreprise)



@admin.register(Lignes_BonCommande)
class BonCommandeClass(admin.ModelAdmin):
    list_display = ('id','ref_commande','produit','qty','total')

@admin.register(Bons_commande)
class BonCommandeClass(admin.ModelAdmin):
    list_display = ('id','number','created_at','etat')
