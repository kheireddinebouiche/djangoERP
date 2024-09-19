from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

TYPE_CLIENT ={
    ('par', 'Particulier'),
    ('ent' , 'Entreprise'),
}

TYPE_RAPPEL = {
    ('mes', 'Message'),
    ('ema', 'Email'),
    ('tel', 'Appel téléphonique'),
}

TYPE_PAIEMENT = {
        ('chq', "Chéque"),
        ('vir', "Virement Bancaire"),
        ('esp', "Espéce"),
    }

TYPE_ETAT = {
    ('enc', 'En cours'),
    ('fin', 'Terminer'),
    ('ann', 'Annuler'),
    ('att', 'En attente'),
}

DEVIS = {
    ('AFG', "Afghanistan"),
    ('ZAF', "Afrique du Sud"),
    ('ALB', "Albanie"),
    ('DZA', "Algérie"),
    ('DEU', "Allemagne"),
    ('AND', "Andorre"),
    ('AGO', "Angola"),
    ('ATG', "Antigua-et-Barbuda"),
    ('SAU', "Arabie Saoudite"),
}

class User(AbstractUser):
    pass

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Note"
        verbose_name_plural="Notes"

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=1000, null=True, blank=True)
    prenom = models.CharField(max_length=1000, null=True, blank=True)
    mobile = models.CharField(max_length=1000, null=True, blank=True)
    date_recrutement = models.DateField(null=True, blank=True)
    salaire_base = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    image =models.ImageField(upload_to='user_image/', blank=True, null=True)


    TYPE_PROFILE = {
        ('adm' , 'Administrateur'),
        ('ven', 'Vendeurs'),
    }
    
    type_profile = models.CharField(max_length=3, null=True, blank=True , choices=TYPE_PROFILE)
    etat = models.CharField(max_length=1, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name='Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name

class Categorie_produit(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now= True, blank=True, null= True)

    class Meta:
        verbose_name='Catégorie de produit'
        verbose_name_plural = 'Catégories'
    def __str__(self):
        return self.label

class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    designation = models.CharField(max_length = 100, blank=True, null = True)
    ref = models.CharField(max_length = 100, blank = True, null= True)
    categorie = models.ForeignKey(Categorie_produit, null=True, blank=True, on_delete=models.SET_NULL)
    TYPE_PROD = {
        ('srv','Service'),
        ('pro','Produit'),
    }
    type_produit = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_PROD)
    code_barre = models.CharField(max_length=100, null=True, blank=True)
    stock_alert = models.CharField(max_length=100, null=True, blank=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    TYPE_TAR = {
        ('h','Horaire'),
        ('j','Jour'),
        ('m','Mois'),
        ('a', 'Année'),
    }
    type_tarifcation = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_TAR)
    cout_produit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    description = models.CharField(max_length=10000, null=True, blank=True)
    disponibilite = models.CharField(max_length=1, null=True, blank=True)
    
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name  = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.designation

TYPE_MOUV = {
    ('ent', 'Entrée'),
    ('sor', 'Sortie'),
}

class Mouvements_produit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    produit = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    type_mouvement = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_MOUV)
    qty = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Mouvement d'un produit"
        verbose_name_plural="Mouvements des produits"

    def __str__(self):
        return self.produit.designation

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, related_name='produit' ,on_delete=models.CASCADE, null=True, blank=True)
    qty = models.CharField(max_length=100, null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Stock"
        verbose_name_plural="Stock"
    
    def __str__(self):
        return self.product.designation

class Prospects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    type_prospect = models.CharField(max_length=100, null=True, blank=True, choices=TYPE_CLIENT)
    observation = models.CharField(max_length=2000, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Prospect"
        verbose_name_plural = "Prospects"

    def __str__(self):
        return self.nom

class RetourProduit(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE)
    ref = models.CharField(max_length=100, null=True, blank=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name="Retour du produit"
        verbose_name_plural = "Retour des produits"
        
    def __str__(self):
        return self.product.designation

class Opportunites(models.Model):
    prospect = models.ForeignKey(Prospects, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Opportunité'
        verbose_name_plural='Opportunités'

    def __str__(self):
        return self.prospect

TYPE_PRIO = {
    ('lo', 'Basse'),
    ('me', 'Medium'),
    ('he', 'Haute'),
}

class Rappels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prospect = models.ForeignKey(Prospects, on_delete=models.CASCADE,null=True, blank=True)
    type_rappel = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_RAPPEL)
    date_rappel = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)
    etat = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_ETAT)
    priority = models.CharField(max_length=2, null=True, blank=True, choices=TYPE_PRIO)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Rappel'
        verbose_name_plural='Rappels'
    
    def __int__(self):
        return self.id

class Clients(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)
    nif = models.CharField(max_length=100, null=True, blank=True)
    nis = models.CharField(max_length=100, null=True, blank=True)
    art = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=3000, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True )
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    reg_commerce = models.CharField(max_length=100, null=True, blank=True)
    type_client = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_CLIENT)

    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name='Client'
        verbose_name_plural='Clients'
        
    def __str__(self):
        return self.designation

class Fournisseurs(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)
    nif = models.CharField(max_length=100, null=True, blank=True)
    nis = models.CharField(max_length=100, null=True, blank=True)
    art = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=3000, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True )
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    reg_commerce = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name='Fournisseur'
        verbose_name_plural = 'Fournisseurs'

    def __str__(self):
        return self.designation

class Devis(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    number = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    client = models.ForeignKey(Clients, null=True, blank=True,on_delete=models.DO_NOTHING)
    date_devis = models.DateField(null=True, blank=True)

   
    ETAT_DEVIS = {
        ('bro', "Brouillon"),
        ('ann', "Annulé"),
        ('fac', "A facturé"),
        ('ter', "Terminer"),
    }
    DELAI_PAIE = {
        ('imm', 'Immédiat'),
        ('rec', 'A réception'),
        ('30j', 'A 30 jours'),
    }
    mode_paiement = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_PAIEMENT)
    delai_paiement = models.CharField(max_length=3, null=True, blank=True, choices=DELAI_PAIE)
    etat = models.CharField(max_length=3, null=True, blank=True, choices=ETAT_DEVIS)
    date_expiration = models.DateField(null=True, blank=True)

    observation = models.TextField(max_length=3000, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_devis_number()
        super().save(*args, **kwargs)

    def generate_devis_number(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%Y')
        last_devis = Devis.objects.filter(number__startswith=date_str).order_by('-number').first()
        if last_devis:
            last_number = int(last_devis.number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{date_str}-{new_number:04}'

    class Meta:
        verbose_name="Devis"
        verbose_name_plural="Devis"

    def __str__(self):
        return self.number

class Ligne_Devis(models.Model):
    devis = models.ForeignKey(Devis, related_name="lines", on_delete=models.CASCADE, null=True, blank=True)
    produit = models.ForeignKey(Products, related_name="product", on_delete=models.CASCADE,null=True, blank=True)
    qty = models.CharField(max_length=100, null=True, blank=True)
    ht = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tva = models.CharField(max_length=10, null=True, blank=True)
    ttc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Ligne du devis"
        verbose_name_plural="Lignes du devis"

    def __str__(self):
        return self.produit.designation

class Facture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    date_facturation = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)


    ETAT_DEVIS = {
        ('bro', "Brouillon"),
        ('ter', "Terminer"),
    }
    DELAI_PAIE = {
        ('imm', 'Immédiat'),
        ('rec', 'A réception'),
        ('30j', 'A 30 jours'),
    }
    
    mode_paiement = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_PAIEMENT)
    delai_paiement = models.CharField(max_length=3, null=True, blank=True, choices=DELAI_PAIE)
    etat = models.CharField(max_length=3, null=True, blank=True, choices=ETAT_DEVIS)

    montant_ht = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100)
    montant_tva = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100)
    montant_ht = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100)

    montant_paye = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100)
    montant_restant = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100)

    observation = models.TextField(max_length=3000, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_facture_number()
        super().save(*args, **kwargs)

    def generate_facture_number(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%Y')
        last_facture = Facture.objects.filter(number__startswith=date_str).order_by('-number').first()
        if last_facture:
            last_number = int(last_facture.number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{date_str}-{new_number:04}'

    class Meta:
        verbose_name="Facture"
        verbose_name_plural="Factures"

    def __str__(self):
        return self.number

class Ligne_Facture(models.Model):
    facture = models.ForeignKey(Facture, related_name="line_facture", on_delete=models.CASCADE, null=True, blank=True)
    produit = models.ForeignKey(Products, related_name="produits", on_delete=models.CASCADE,null=True, blank=True)
    qty = models.CharField(max_length=100, null=True, blank=True)
    ht = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tva = models.CharField(max_length=10, null=True, blank=True)
    ttc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Ligne de facture"
        verbose_name_plural="Lignes du facture"

    def __str__(self):
        return self.produit.designation

class Facture_Avoir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    ref_facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)
    montant_total = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100)
    motifs = models.CharField(max_length=1000, null=True, blank=True)

    ETAT_AVOIR = {
        ('bro', "Brouillon"),
        ('ter', "Terminer"),
    }
    etat = models.CharField(max_length=3, null=True, blank=True, choices=ETAT_AVOIR)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_facture_avoir_number()
        super().save(*args, **kwargs)

    def generate_facture_avoir_number(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%Y')
        last_facture = Facture_Avoir.objects.filter(number__startswith=date_str).order_by('-number').first()
        if last_facture:
            last_number = int(last_facture.number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{date_str}-{new_number:04}'

    class Meta:
        verbose_name="Facture d'avoire"
        verbose_name_plural="Factures d'avoire"

    def __str__(self):
        return self.number

class LigneFactureAvoir(models.Model):

    ref_facture_avoir = models.ForeignKey(Facture_Avoir, null=True, blank=True, on_delete=models.CASCADE)
    produit = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE)
    qty = models.CharField(max_length=100, null=True, blank=True)
    ht = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tva = models.CharField(max_length=10, null=True, blank=True)
    ttc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Ligne avoir",
        verbose_name_plural = "Lignes avoir"

    def __str__(self):
        return self.ref_facture_avoir

class Bons_commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=1000, null=True, blank=True)
    date_du_bon = models.DateField(null=True, blank=True)
    date_livraison = models.DateField(null=True, blank=True)

    ref_devis = models.CharField(max_length=1000, null=True, blank=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_bon_commande_number()
        super().save(*args, **kwargs)

    def generate_bon_commande_number(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%Y')
        last_bon_commande = Bons_commande.objects.filter(number__startswith=date_str).order_by('-number').first()
        if last_bon_commande:
            last_number = int(last_bon_commande.number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{date_str}-{new_number:04}'

    class Meta:
        verbose_name="Bon de commande"
        verbose_name_plural = "Bons de commande"
    
    def __str__(self):
        return self.number

class Lignes_BonCommande(models.Model):
    pass

class Bons_livraison(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=1000, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseurs, null=True, blank=True, on_delete=models.SET_NULL)
    date_du_bon = models.DateField(null=True, blank=True)
    lieu_livraison = models.CharField(max_length=1000, null=True, blank=True)

    observation = models.CharField(max_length=1000, null=True, blank=True)

    montant_total = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    montant_paye =  models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    montant_restant = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_bon_livraison_number()
        super().save(*args, **kwargs)

    def generate_bon_livraison_number(self):
        now = datetime.datetime.now()
        date_str = now.strftime('%Y')
        last_bon_livraison = Bons_livraison.objects.filter(number__startswith=date_str).order_by('-number').first()
        if last_bon_livraison:
            last_number = int(last_bon_livraison.number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{date_str}-{new_number:04}'

    class Meta:
        verbose_name="Bon de livraison"
        verbose_name_plural = "Bons de livraison"

    def __str__(self):
        return self.number

class Lignes_bon_livraison(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bon_livraison = models.ForeignKey(Bons_livraison, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)

    qty = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Ligne du bon de livraison"
        verbose_name_plural = "Lignes du bon de livraison"

    def __str__(self):
        return self.product.designation

class PaiementClient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)
    montant_paiement = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=3, null=True, blank=True, choices=TYPE_PAIEMENT)
    ref_paiement = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name="Paiement facture"
        verbose_name_plural="Paiements facture"
        
    def __str__(self):
        return self.facture.number

class GeneralSettings(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    prefix_devis = models.CharField(max_length=1000, null=True, blank=True)
    prefix_facture = models.CharField(max_length=1000, null=True, blank=True)
    prefix_avoir = models.CharField(max_length=1000, null=True, blank=True)
    devise = models.CharField(max_length=3, null=True, blank=True, choices=DEVIS)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)

    print_ticket_pdf = models.BooleanField(null=True, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Configuration"
        verbose_name_plural="Configuration"

    def __int__(self):
        return self.user

class Infos_Entreprise(models.Model):

    designation = models.CharField(max_length=100, null=True, blank=True)
    nif = models.CharField(max_length=100, null=True, blank=True)
    nis = models.CharField(max_length=100, null=True, blank=True)
    art = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=3000, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True )
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    reg_commerce = models.CharField(max_length=100, null=True, blank=True)
    iban = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name='Mon Entreprise'
        
    def __str__(self):
        return self.designation

class Caisse(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    num = models.CharField(max_length=100, null=True, blank=True)
    etat = models.CharField(max_length=1, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.num:
            self.num= self.generate_caisse_number()
        super().save(*args, **kwargs)

    def generate_caisse_number(self):
        
        last_caisse = Caisse.objects.order_by('-num').first()
        if last_caisse:
            last_number = int(last_caisse.num[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{new_number:09}'

    class Meta:
        verbose_name="Caisse"
        verbose_name_plural="Caisses"

    def __str__(self):
        return self.num

class SessionVente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    caisse = models.ForeignKey(Caisse, null=True, blank=True, on_delete=models.CASCADE)
    num = models.CharField(max_length=100, null=True, blank=True)
    etat = models.CharField(max_length=1, null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.num:
            self.num= self.generate_session_number()
        super().save(*args, **kwargs)

    def generate_session_number(self):
        
        last_session = SessionVente.objects.order_by('-num').first()
        if last_session:
            last_number = int(last_session.num[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'{new_number:09}'

    class Meta:
        verbose_name="Session de vente"
        verbose_name_plural = "Sessions de vente"

    def __str__(self):
        return self.num

class LigneCaisse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(SessionVente, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_total = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    qty = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Ligne caisse"
        verbose_name_plural = "Lignes caisse"
    
    def __int__(self):
        return self.product

class Tva(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    taux = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Taux"
        verbose_name_plural = "Taux TVA"

    def __str__(self):
        return self.description