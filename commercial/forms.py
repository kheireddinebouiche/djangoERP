from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class newEntrepriseForm(forms.ModelForm):
    class Meta:
        model = Infos_Entreprise
        fields = ['designation','nif','nis','art','adresse','mobile','fax','email','reg_commerce']
        
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Veuillez entrer la designation de l'entreprise", 'id': 'designation'}),
            'nif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° NIF'}),
            'nis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° NIS'}),
            'art': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° ARTICLE'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse siége social'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Mobile'}),
            'fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° FAX'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMAIL professionnel'}),
            'reg_commerce': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° du registre commerce'}),

        }
   
class CreateNewDevis(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['client','mode_paiement','delai_paiement','etat','date_expiration','observation','date_devis']
        labels = {
            'client' : "Désignation du client",
            'mode_paiement' : "Mode de paiement",
            'delai_paiement':"Délai de paiement",
            'etat' : "Statut du devis",
            'date_expiration' : "Devis valide au ",
            'obeservation' : "Observations",
            'date_devis' : "Date du devis",
        }
        widgets = {
            'client' : forms.Select(attrs={'class' : 'form-control'}),
            'mode_paiement' : forms.Select(attrs={'class' : 'form-control'}),
            'delai_paiement' : forms.Select(attrs={'class': 'form-control'}),
            'date_expiration' : forms.TextInput(attrs={'class': 'form-control','type':'date'}),
            'observation' : forms.Textarea(attrs={'class':'form-control'}),
            'etat':forms.Select(attrs={'class': 'form-control'}),
            'date_devis' : forms.TextInput(attrs={'class': 'form-control','type':'date'}),
        }

class CreateNewFacture(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client','mode_paiement','delai_paiement','etat','observation','date_facturation']
        labels = {
            'client' : "Désignation du client",
            'mode_paiement' : "Mode de paiement",
            'delai_paiement':"Délai de paiement",
            'etat' : "Statut du devis",
            'obeservation' : "Observations",
            'date_facturation' : "Date de facturation",
        }
        widgets = {
            'client' : forms.Select(attrs={'class' : 'form-control'}),
            'mode_paiement' : forms.Select(attrs={'class' : 'form-control'}),
            'delai_paiement' : forms.Select(attrs={'class': 'form-control'}),
            
            'observation' : forms.Textarea(attrs={'class':'form-control'}),
            'etat':forms.Select(attrs={'class': 'form-control'}),
            'date_facturation' : forms.TextInput(attrs={'class': 'form-control','type':'date'}),
        }

class RappelForm(BSModalModelForm):
    class Meta:
        model = Rappels
        fields = ['prospect','type_rappel','date_rappel','observation','etat']
        widgets = {
            'prospect' : forms.TextInput(attrs={'class':'form-control'}),
            'type_rappel' : forms.Select(attrs={'class':'form-control'}),
            'date_rappel' : forms.TextInput(attrs={'class':'form-control'}),
            'observation' : forms.TextInput(attrs={'class':'form-control'}),
            'etat' : forms.Select(attrs={'class':'form-control'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class ClientAddForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['designation','nif','nis','art','adresse','mobile','fax','email','type_client','reg_commerce']
        
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Veuillez entrer la designation de l'entreprise", 'id': 'designation'}),
            'nif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° NIF'}),
            'nis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° NIS'}),
            'art': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° ARTICLE'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse siége social'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Mobile'}),
            'fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° FAX'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMAIL professionnel'}),
            'type_client': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Type du client'}),
            'reg_commerce': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° du registre commerce'}),

        }

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['type_produit','designation','ref','categorie','code_barre','prix_vente','prix_achat','cout_produit','image','stock_alert']
        labels = {
            'designation' : "Désignation du produit :",
            'categorie' : "Veuillez séléctionner la catégorie du produit/Article :",
            'code_barre' : "Code à barre :",
            'prix_vente' : "Prix de vente :",
            'prix_achat' : "Prix d'achat :",
            'cout_produit' : "Coût du produit :",
            'image' : "Image du produit",
            'ref' : "Référence du produit :",
            'stock_alert' : "Quantité minimum dans le stock :",
            'type_produit' : "Type de produit :"
            
        }
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Veuillez entrer la designation du produit", 'id': 'label','required' : 'True'}),
            'ref': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer la référence', 'id':'ref','required' : 'True'}),
            'categorie' : forms.Select(attrs={'class':'form-control', 'id':'cat'}),
            'prix_vente' : forms.NumberInput(attrs={'class':'form-control', 'id':'vente','placeholder' :"Prix de d'achat du produit",'required' : 'True'}),
            'prix_achat' : forms.NumberInput(attrs={'class':'form-control', 'id':'achat', 'placeholder' :'Prix de vente du produit','required' : 'True'}),
            'cout_produit' : forms.NumberInput(attrs={'class':'form-control', 'id':'cout_produit','placeholder':'Cout de fabrication du produit'}),
            'code_barre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code à barre du produit', 'id':'codebarre', 'required' : 'True'}),
            'stock_alert': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Le stock minimum du produit', 'id':'stockmin', 'required' : 'False'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'image'}),
            'type_produit' : forms.Select(attrs={'class':'form-control', 'id':'type_prod'}),
        
           
        }

class ServiceAddForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['type_produit','designation','ref','categorie','code_barre','prix_vente','prix_achat','cout_produit','image','stock_alert']
        labels = {
            'designation' : "Désignation du produit :",
            'categorie' : "Veuillez séléctionner la catégorie du produit/Article :",
            'code_barre' : "Code à barre :",
            'prix_vente' : "Prix de vente :",
            'prix_achat' : "Prix d'achat :",
            'cout_produit' : "Coût du produit :",
            'image' : "Image du produit",
            'ref' : "Référence du produit :",
            'stock_alert' : "Quantité minimum dans le stock :",
            'type_produit' : "Type de produit :"
            
        }
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Veuillez entrer la designation du produit", 'id': 'label','required' : 'True'}),
            'ref': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer la référence', 'id':'ref','required' : 'True'}),
            'categorie' : forms.Select(attrs={'class':'form-control', 'id':'cat'}),
            'prix_vente' : forms.NumberInput(attrs={'class':'form-control', 'id':'vente','placeholder' :"Prix de d'achat du produit",'required' : 'True'}),
            'prix_achat' : forms.NumberInput(attrs={'class':'form-control', 'id':'achat', 'placeholder' :'Prix de vente du produit','required' : 'True'}),
            'cout_produit' : forms.NumberInput(attrs={'class':'form-control', 'id':'cout_produit','placeholder':'Cout de fabrication du produit'}),
            'code_barre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code à barre du produit', 'id':'codebarre', 'required' : 'True'}),
            'stock_alert': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Le stock minimum du produit', 'id':'stockmin', 'required' : 'False'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'image'}),
            'type_produit' : forms.Select(attrs={'class':'form-control', 'id':'type_prod'}),
        
           
        }

class ProductCategoriForm(forms.ModelForm):
    class Meta:
        model = Categorie_produit
        fields = ['label']
        labels = {
            'label' : 'La désignation de la catégorie',
        }
        widgets= {
            'label' : forms.TextInput(attrs={'class' : 'form-control', 'id' : 'label', 'placeholder' : 'Veuillez entrer un nom/description catégorie du produit'})
        }

class FournisseurAddForm(forms.ModelForm):
    class Meta:
        model = Fournisseurs
        fields = ['designation','nif','nis','art','adresse','mobile','fax','email','reg_commerce']
        
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Veuillez entrer la designation de l'entreprise", 'id': 'designation'}),
            'nif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° NIF'}),
            'nis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° NIS'}),
            'art': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le N° ARTICLE'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse siége social'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Mobile'}),
            'fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° FAX'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMAIL professionnel'}),
            'reg_commerce': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° du registre commerce'}),
        }

class OpportuniteForm(forms.ModelForm):
    class Meta:
        model = Opportunites
        fields = ['prospect', 'description']
        widgets = {
            'prospect' : forms.Select(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
        }

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['text']
        labels = {
            'text' : 'Contenue de votre note'
        }
        widgets = {
            'text' : forms.TextInput(attrs={'class':'form-control', 'id' :'note_id'})
        }

class ProspectForm(forms.ModelForm):
    class Meta:
        model = Prospects
        fields = ['nom', 'prenom', 'type_prospect']

        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'prenom' : forms.TextInput(attrs={'class':'form-control'}),
            'type_prospect' : forms.Select(attrs={'class' : 'form-control'})
        }

class ParamGenForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = ['prefix_devis','prefix_facture','devise','logo','prefix_avoir']
        labels = {
            'prefix_devis': "Préfixe des devis :",
            'prefix_facture': "Préfix des factures",
            'prefix_avoir' : "Préfix des factures d'avoir",
            'devise': "Devise :",
            'logo' : "Logo de l'entreprise",
            'print_ticket_pdf' : "Type de document point de vente :"
        }
        widgets = {
            'prefix_devis' : forms.TextInput(attrs={'class':'form-control', 'id': 'prefixdevis'}),
            'prefix_facture' : forms.TextInput(attrs={'class':'form-control', 'id': 'prefixfacture'}),
            'prefix_avoir' : forms.TextInput(attrs={'class':'form-control', 'id': 'prefixAvoir'}),
            'devise' : forms.Select(attrs={'class':'form-control', 'id': 'devise'}),
            'logo' : forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'image'}),
            'print_ticket_pdf': forms.RadioSelect(attrs={'class' : 'form-control', 'id' : 'selec_impr'}),
        }

class CreateBonLivraisonForm(forms.ModelForm):
    class Meta:
        model = Bons_livraison
        fields = ['fournisseur','date_du_bon','lieu_livraison','observation']
        pass