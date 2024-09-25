from django.contrib import admin
from django.urls import path
from .views import *

app_name="commercial"



urlpatterns = [

    path('invoice/<int:invoice_id>/pdf/', generate_invoice_pdf, name='generate_invoice_pdf'),

    path('', Index, name='index'),
    path('contact/', contact_view, name='contact'),
    path('mon-profile/', MyProfile, name="mon_profile"),
    path('configuration/', configuration, name="configuration"),
    path('configuration-infos-entreprise/', ConfiugreMyEntreprise, name="ConfiugreMyEntreprise"),

    # GESTION DES PAIEMENTS ###############################################################################
    path('ventes/paiements/liste-des-paiements/', listePaiement, name="listePaiement"),
    path('ApiFetchListePaiement/',ApiFetchListePaiement ,name="ApiFetchListePaiement"),
    path('AddPaiement', AddPaiement, name="AddPaiement"),
    # GESTION DES PAIEMENTS ###############################################################################

    path('produits/retours-produit/',ListRetourProduit, name="ListRetourProduit"),
    path('ApiGetRetourProduitItem', ApiGetRetourProduitItem, name="ApiGetRetourProduitItem"),
    path('DeleteRetourLine', DeleteRetourLine, name="DeleteRetourLine"),

    # GESTION DES DEVIS ###################################################################################
    path('ventes/devis/liste-des-devis/', listeDevis, name="listeDevis"),
    path('ventes/nouveau-devis/', add_devis, name="add_devis"),
    path('ventes/devis/configuration-du-devis/<int:pk>/', addToDevis, name="addToDevis"),
    path('ApiListeDevis', ApiListeDevis , name="ApiListeDevis"),
    path('ApiFecthDevisLigne/', ApiFecthDevisLigne, name="ApiFecthDevisLigne"),
    path('ApiFetchFactureItem/', ApiFetchFactureItem, name="ApiFetchFactureItem"),
    path('deleteDevis', deleteDevis, name="deleteDevis"),
    path('addNewDevisProduct', addNewDevisProduct, name="addNewDevisProduct"),
    path('deleteLigneDevis', deleteLigneDevis, name="deleteLigneDevis"),
    path('validateDevis/<int:pk>/', validateDevis, name="validateDevis"),
    path('makeDevisBrouillon/<int:pk>/', makeDevisBrouillon, name="makeDevisBrouillon"),
    path('GenFactureFromDevis/<int:pk>/', GenFactureFromDevis, name="GenFactureFromDevis"), 
    path('ventes/factures/details-facture/<int:pk>/', detailFacture, name="detailFacture"),
    path('ventes/factures/liste-des-factures/', page_liste_facture, name="page_liste_facture"),
    path('liste_Facture', liste_Facture, name="liste_Facture"),
    path('ventes/factures/configuration-facture/<int:pk>/', config_facture, name="config_facture"),
    path('ApiUpdateFacture/',ApiUpdateFacture, name="ApiUpdateFacture"),
    path('valideInvoice', valideInvoice, name="valideInvoice"),

    path('ventes/nouvelles-facture/', add_facture, name="add_facture"),
    path('addNewFactureProduct', addNewFactureProduct ,name="addNewFactureProduct"),
    path('deleteLigneFacture', deleteLigneFacture, name="deleteLigneFacture"),
    path('deleteFacture', deleteFacture, name="deleteFacture"),

    path('ventes/facture-avoir/', FactureAvoirePage ,name="FactureAvoirePage"),
    path('APIGetFactureAvoir', APIGetFactureAvoir, name="APIGetFactureAvoir"),
    path('ConfigAvoir', CreateAvoir, name="ConfigAvoir"),
    path('DeleteFactureAvoir', deleteFactureAvoir, name="DeleteFactureAvoir"),
    path('ventes/facture-avoir/configuration/<int:pk>/', AvoirConf, name="AvoirConf"),
    path('ApiFetchFactureAvoirItem', ApiFetchFactureAvoirItem, name="ApiFetchFactureAvoirItem"),
    path('ApiFetchLigneAvoirDetails', ApiFetchLigneAvoirDetails, name="ApiFetchLigneAvoirDetails"),
    path('ApiUpdateLigneFactureAvoir', ApiUpdateLigneFactureAvoir, name="ApiUpdateLigneFactureAvoir"),

    # GESTION DES DEVIS ###################################################################################

    # GESTION DES USERS ###################################################################################
    path('gestion-des-utilisateurs/liste-des-utilisateurs/', PageListeUtilisateur, name="ListeDeUtilisateurs"),
    path('ListeDeUtilisateurs/', ListeDeUtilisateurs, name="ListeDeUtilisateursPage"),
    path('gestion-des-utilisateurs/nouveau-utilisateur/',addNewUserProfile, name="addNewUserProfile"),
    path('GetProfileInfo', GetProfileInfo, name="GetProfileInfo"),
    path('updateProfile', updateProfile, name="updateProfile"),
    path('addNewUserProfile', addNewUserProfile, name="addNewUserProfile"),
    path('gestion-des-utilisateurs/details-utilisateurs/<int:pk>/',userDetails, name="user_details"),
    path('deleteUser', deleteUser, name="deleteUser"),
    # GESTION DES USERS ###################################################################################

    # GESTION DU POS ######################################################################################
    path('pos-dashboard/',PosDashboard,name="pos_dashboard"),
    path('point-de-vente/vente', pos, name='pos'),
    path('point-de-vente/lignes-caisse/', ligneCaisse, name="lignes_caisse"),
    path('nouvelle-session/', new_session, name="new_session"),
    path('cloture-de-la-caisse/<int:pk>/',clotureCaisse,name='colture_caisse'),
    path('ajouter-produit-vente/', add_product_to_sale, name="add_product_to_sale"),
    path('update-product-qty/', update_product_qty, name='update_product_qty'),
    path('point-de-vente/liste-des-bons/',listBons,name="listBons"),
    path('point-de-vente/liste-des-ventes/', listDesVente, name="listDesVente"),
    path('delete-product-from-sale/',remove_product_from_sale, name="remove_product_from_sale"),
    path('point-de-vente/historique-des-caisses/',list_caisse, name="list_caisse"),
    path('liste_session_caisse', liste_session_caisse, name="liste_session_caisse"),
    # GESTION DU POS ######################################################################################

    # GESTION DES RAPPELS #################################################################################
    path('rappels/liste-des-rappels/', ListeDesRappels , name="liste_rappele"),
    #path('rappels/nouveau-rappel/', RappelCreateView.as_view(), name="nouveau_rappel"),
    path('rappels/nouveau-rappel/', nouveau_rappele, name="new_rappel"),
    # GESTION DES RAPPELS #################################################################################

    # Gestion des clients #################################################################################
    path('formulaire-ajout-client/', client_view, name="add-client"),
    path('liste-des-clients/', client_liste, name='client-list'),
    path('update-client/<int:pk>/', client_update, name="client_update"),
    path('clients/details-du-client/<int:pk>/', clientDetails, name="clientDetails"),

    path('prospects/liste-des-prospects/', list_prospect, name="list_prospect"),
    path('prospects/nouveau-prospect/', add_prospects, name="nouveau_prospect"),

    path('opportunites/liste-des-opportunites/', liste_opportunite, name="liste_opportunite"),
    path('opportunites/nouvelle-opportunites/', add_opportunite, name="add_opportunite"),
    
    # Fin Gestion des clients #############################################################################

    # Gestion des fournisseurs ############################################################################
    path('fournisseurs/liste-des-fournisseurs/', liste_fournisseur, name="liste_fournisseur"),
    path('fournisseurs/nouveau-fournisseur/', nouveau_fournisseur, name="nouveau_fournisseur"),
    path('fournisseurs/modification-des-donnees-fournisseur/<int:pk>/', update_fournisseur, name="update_fournisseur"),
    # Fin Gestion des fournisseurs ########################################################################

    # Gestion des produits ################################################################################
    path('gestion-des-produits/liste-des-produits/', product_liste, name='product-liste'),
    path('gestion-des-produits/nouveau-produit/', add_product, name='nouveau-produit'),
    path('gestion-des-produits/details-produit/<int:pk>/', details_produit, name="details-produit"),
    path('gestion-des-produits/mise-a-jour-produit/<int:pk>/', update_produit, name="update_produit"),
    path('delete-product/<int:pk>/', delete_product ,name="delete_product"),
    path('ApiFetchProductDetails', ApiFetchProductDetails, name="ApiFetchProductDetails"),

    path('gestion-des-produits/liste-des-services/', PageListeService, name="PageListeService"),
    path('ApiLoadService', ApiLoadService, name="ApiLoadService"),
    path('AddNewService', AddNewService, name="AddNewService"),
    path('ApiGetServiceDetails', ApiGetServiceDetails, name="ApiGetServiceDetails"),
    path('ApiUpdateService', ApiUpdateService, name="ApiUpdateService"),
    path('ApiDeleteService', ApiDeleteService, name="ApiDeleteService"),

    # Fin Gestion des produits ############################################################################

    # Gestion du stock ####################################################################################
    
    path('stock/etat-du-stock/',etat_stock, name="etat_stock"),    
    path('sotck/nouvelle-entre-stock/',nouvelle_entree_stock, name="nouvelle_entree_stock"),
    path('stock/mouvements-des-produits/',PageMouvementListe, name="mouvement_des_produits"),
    path('ApiGetMouvItem', ApiGetMouvItem, name="ApiGetMouvItem"),
    path('DeleteMouvementLine', DeleteMouvementLine, name="DeleteMouvementLine"),
    path('ApiDetailsMouvement', ApiDetailsMouvement, name="ApiDetailsMouvement"),

    # Fin gestion du stock  ###############################################################################

    # Categorie des produits ##############################################################################
    path('gestion-des-produits/categories/liste/',list_categorie, name='categorie_list'),
    path('gestion-des-produits/categories/update/',update_categorie, name='update_categorie'),
    path('gestion-des-produits/produit-par-categorie/', categorieProduit, name="categorieProduit"),
    path('ApiFetchProductCat', ApiFetchProductCat, name="ApiFetchProductCat"),

    path('ApiListCategorieProduit', ApiListCategorieProduit, name="ApiListCategorieProduit"),
    path('ApiGetCategorieDetails', ApiGetCategorieDetails, name="ApiGetCategorieDetails"),
    path('ApiAddCategorie', ApiAddCategorie, name="ApiAddCategorie"),
    path('ApiUpdateCategorie', ApiUpdateCategorie, name="ApiUpdateCategorie"),
    path('ApiDeleteCategorie', ApiDeleteCategorie, name="ApiDeleteCategorie"),
    # Fin Categorie des produits ##########################################################################

    # Categorie des notes #################################################################################
    path('notes/mes-notes/',liste_notes, name="mes_notes"),
    path('notes/nouvelle-note/',add_note, name="ajouter_note"),
    # Categorie des notes #################################################################################

    path('configuration/facturation/liste-des-taux/',PageTva, name="PageTva"),
    path('ApiGetListeTva', ApiGetListeTva, name="ApiGetListeTva"),
    path('ApiAddTaux', ApiAddTaux, name="ApiAddTaux"),
    path('ApiDeleteTaux', ApiDeleteTaux, name="ApiDeleteTaux"),
    path('ApiGetTauxDetails', ApiGetTauxDetails, name="ApiGetTauxDetails"),
    path('ApiUpdateTaux', ApiUpdateTaux, name="ApiUpdateTaux"),

    ################### GESTION DES COMMANDES #############################################################
    path('achats/bons-de-commandes/',PageListeCommande, name="PageListeCommande"),
    path('ApiGetListeCommande',ApiGetListeCommande,name="ApiGetListeCommande"),
    path('achats/bons-de-commandes/nouvelle-commande/',CreateBonCommande, name="CreateBonCommande"),
    path('achat/bons-de-commandes/configuration/<int:pk>/',ConfCommande, name="ConfCommande"),
    path('ApiGetProducts/',ApiGetProducts,name="ApiGetProducts"),
    path('ApiConfirmAddNewProduct',ApiConfirmAddNewProduct,name="ApiConfirmAddNewProduct"),
    path('ApiFetchCommandeItem',ApiFetchCommandeItem, name="ApiFetchCommandeItem"),
    path('ApiAddCommandeLine', ApiAddCommandeLine, name="ApiAddCommandeLine"),
    path('ApiDeleteLigneCommande',ApiDeleteLigneCommande,name="ApiDeleteLigneCommande"),
    path('ApiDeleteBonCommande',ApiDeleteBonCommande,name="ApiDeleteBonCommande"),
    path('ApiGetCommandeDetails', ApiGetCommandeDetails, name="ApiGetCommandeDetails"),
    path('ApiUpdateCommande',ApiUpdateCommande,name="ApiUpdateCommande"),
    path('ApiLoadTotalCommande',ApiLoadTotalCommande,name="ApiLoadTotalCommande"),
    path('ApiUpdateQty', ApiUpdateQty, name="ApiUpdateQty"),
    path('ApiValidateBonCommande', ApiValidateBonCommande, name="ApiValidateBonCommande"),
    path('ApiMakeCommandeBrouillon', ApiMakeCommandeBrouillon, name="ApiMakeCommandeBrouillon"),
    ################### GESTION DES COMMANDES #############################################################

]