from django.shortcuts import render, redirect, reverse,get_object_or_404
from django.http import JsonResponse, HttpResponse
from .forms import *
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from bootstrap_modal_forms.generic import BSModalCreateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.db.models import Count
from num2words import num2words
import os
from django.conf import settings


def convert_decimal_to_words(number):
    # Séparer la partie entière et la partie décimale
    partie_entière, partie_décimale = str(number).split(".")

    # Convertir la partie entière en mots
    partie_entière_en_mots = num2words(int(partie_entière), lang='fr')

    # Convertir la partie décimale en mots (deux chiffres maximum)
    partie_décimale_en_mots = num2words(int(partie_décimale[:2]), lang='fr')

    # Combiner les deux parties
    return f"{partie_entière_en_mots} virgule {partie_décimale_en_mots}"

@login_required(login_url='/login/')
def generate_invoice_pdf(request, invoice_id):
    # Récupérer la facture à partir de l'ID
    invoice = Facture.objects.get(pk=invoice_id)
    conf = GeneralSettings.objects.get()
    items = Ligne_Facture.objects.filter(facture = invoice)

    logo_path = os.path.join(settings.MEDIA_ROOT, str(conf.logo))

    montant_ht = Ligne_Facture.objects.filter(facture=invoice).aggregate(total=Sum('ht'))['total']
    montant_ttc = Ligne_Facture.objects.filter(facture=invoice).aggregate(total=Sum('ttc'))['total']
    montant_tva = montant_ttc-montant_ht

    chiffreEnLettre = convert_decimal_to_words(montant_ttc)
    
    # # Récupérer les lignes de facture associées
    # items = invoice.items.all()

    # Créer le contexte pour le template
    context = {
        'invoice': invoice,
        'conf' : conf,
        'items': items,
        'montant_ht' : montant_ht,
        'montant_ttc': montant_ttc,
        'montant_tva': montant_tva,
        'chiffreEnLettre' : chiffreEnLettre,
        'logo_path' : logo_path,
    }

    # Charger le template HTML et le rendre en tant que chaîne
    html_string = render_to_string('template_facture.html', context)

    # Créer une réponse HTTP pour le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="FACTURE_{invoice.number}.pdf"'

    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

@login_required(login_url='/login/')
def generate_quot_pdf(request, quot_id):
    # Récupérer la facture à partir de l'ID
    quot = Devis.objects.get(pk=quot_id)
    conf = GeneralSettings.objects.get()
    items = Ligne_Devis.objects.filter(devis = quot)

    montant_ht = Ligne_Devis.objects.filter(devis=quot).aggregate(total=Sum('ht'))['total']
    montant_ttc = Ligne_Devis.objects.filter(facture=quot).aggregate(total=Sum('ttc'))['total']
    montant_tva = montant_ttc-montant_ht

    # # Récupérer les lignes de facture associées
    # items = invoice.items.all()

    # Créer le contexte pour le template
    context = {
        'quot': quot,
        'conf' : conf,
        'items': items,
        'montant_ht' : montant_ht,
        'montant_ttc': montant_ttc,
        'montant_tva': montant_tva,
    }

    # Charger le template HTML et le rendre en tant que chaîne
    html_string = render_to_string('template_devis.html', context)

    # Créer une réponse HTTP pour le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="DEVIS_{quot.number}.pdf"'

    # Convertir le HTML en PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

@login_required(login_url='/login/')
def Index(request):

    facture = Facture.objects.filter(etat="ter").count()
    client = Clients.objects.all().count()
    fournisseur = Fournisseurs.objects.all().count()
    products = Products.objects.all().count()

    context = {
        'facture' :facture,
        'client' : client,
        'founisseur' : fournisseur,
        'products' : products,
    }

    return render(request, 'index-2.html', context)

@login_required(login_url='/login/')
def MyProfile(request):
    return render(request, 'app-profile.html')

def contact_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required(login_url='/login/')
def ConfiugreMyEntreprise(request):
    
    try:
        ent = Infos_Entreprise.objects.get()
        form = newEntrepriseForm(instance=ent)
        if request.method == "POST":
            form = newEntrepriseForm(request.POST, instance=ent)
            if form.is_valid():
                form.save()

                messages.success(request,"Les informations de votre entreprise ont été modifié")

                return redirect('commercial:ConfiugreMyEntreprise')
        else:

            context = {
                'form' : form
            }
            return render(request,"infos_entreprise.html", context)

    except ObjectDoesNotExist:

        form = newEntrepriseForm()
        if request.method == "POST":
            form = newEntrepriseForm(request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, "Les informations de votre entreprise ont été enregistrer")

                return redirect('commercial:ConfiugreMyEntreprise')
            
        else:

            context = {
                'form' : form
            }
            return render(request,"infos_entreprise.html", context)

###################### GESTION DES PAIEMENTS ########################################
@login_required(login_url='/login/')
def listePaiement(request):
    conf = GeneralSettings.objects.get()
    factures = Facture.objects.filter(etat="ter")
    context = {
        'conf' : conf,
        'factures' : factures,
    }
    return render(request, "liste_paiements.html", context)

@login_required(login_url='/login/')
def ApiFetchListePaiement(request):
    liste = PaiementClient.objects.all().values('id','facture','facture__number','montant_paiement','mode_paiement','date_paiement','ref_paiement')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def AddPaiement(request):
    if request.method == "GET":

        id_facture = request.GET.get('id_facture')
        montant_paiement = request.GET.get('montant_paiement')
        date_paiement = request.GET.get('date_paiement')
        ref_paiement = request.GET.get('ref_paiement')

        facture  =Facture.objects.get(id = id_facture)

        montant_ttc = Ligne_Facture.objects.filter(facture = facture).aggregate(total=Sum('ttc'))['total']
        montant_paye = PaiementClient.objects.filter(facture = facture).aggregate(total=Sum('montant_paiement'))['total']

        montant_res = montant_ttc - montant_paye
     

        if float(montant_res) > float(montant_paiement):

            new_paiement = PaiementClient(
                user = request.user,
                facture = facture,
                date_paiement = date_paiement,
                montant_paiement = montant_paiement,
                ref_paiement = ref_paiement
            )
            new_paiement.save()

            messages.success(request,"Le paiement a été ajouter avec succès")
        
        else:

            messages.error(request,"Le montant payé est supperieur au montant restant à payé")

        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})


###################### GESTION DES PAIEMENTS ########################################

########################## GESTION DES RETOURS ##################################################
@login_required(login_url='/login/')
def ListRetourProduit(request):
    return render(request, 'liste-des-retours-produits.html')

@login_required(login_url='/login/')
def ApiGetRetourProduitItem(request):
    liste = RetourProduit.objects.all().values('id','product__designation','product__ref','ref','observation','created_at')
    for fac in liste:
        fac_instance = RetourProduit.objects.get(id=fac['id'])
       
        fac['created_at'] = fac['created_at'].strftime('%Y-%m-%d')

    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def DeleteRetourLine(request):
    if request.method == "GET":
        id_line_retour = request.GET.get('retour_line_id')
        obj = RetourProduit.objects.filter(id = id_line_retour)
        obj.delete()

        messages.success(request, "L'opération à été effectuer avec succès")

        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})


########################## GESTION DES RETOURS ##################################################

#################### GESTION DES DEVIS ET FACTURES ##############################################
@login_required(login_url='/login/')
def listeDevis(request):
    return render(request, 'liste_des_devis.html')

def ApiListeDevis(request):
    liste = Devis.objects.all().values('id','number','date_devis','date_expiration','mode_paiement','client','client__designation','etat')

    # Convertir la valeur du champ type_profile en son label
    for devis in liste:
        devis_instance = Devis.objects.get(id=devis['id'])
        devis['etat_label'] = devis_instance.get_etat_display()

    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def add_devis(request):
    form = CreateNewDevis()
    if request.method == "POST":
        form = CreateNewDevis(request.POST)
        if form.is_valid():
            
            client = form.cleaned_data.get('client')
            observation = form.cleaned_data.get('observation')
            mode_paiement  = form.cleaned_data.get('mode_paiement') 
            delai_paiement = form.cleaned_data.get('delai_paiement')
            etat = form.cleaned_data.get('etat')
            date_expiration = form.cleaned_data.get('date_expiration')
            date_devis = form.cleaned_data.get('date_devis')

            new_devis = Devis(
                user = request.user,
                client = client,
                observation = observation,
                mode_paiement = mode_paiement,
                delai_paiement = delai_paiement,
                etat = "bro",
                date_expiration = date_expiration,
                date_devis = date_devis
            )

            new_devis.save()
            

            messages.success(request,"Le devis à été créer avec succès")
            return redirect('commercial:addToDevis', new_devis.id)
    
    context = {
        'form' : form,
    }
    return render(request, 'add_devis.html', context)

@login_required(login_url='/login/')
def detailsDevis(request, pk):
    pass

@login_required(login_url='/login/')
def validateDevis(request, pk):
    obj = Devis.objects.get(id = pk)

    obj.etat = "fac"
    obj.save()
    messages.success(request,"Le devis à été validé avec succès")

    return redirect('commercial:addToDevis', obj.id)

@login_required(login_url='/login/')
def makeDevisBrouillon(request, pk):
    obj = Devis.objects.get(id = pk)

    obj.etat = "bro"
    obj.save()
    messages.success(request,"Opération effectué avec succès")

    return redirect('commercial:addToDevis', obj.id)

@login_required(login_url='/login/')
def deleteDevis(request):
    if request.method == "GET":

        id_devis = request.GET.get('id_devis')
        obj = Devis.objects.get(id=id_devis)

        if obj.etat == "ter":

            messages.success(request,'Suppression impossible, Le devis à été valider et fait référence à une facture')
            
            # Extraire les messages
            response_messages = []
            for message in messages.get_messages(request):
                response_messages.append({
                    "message": message.message,
                    "tags": message.tags,
                })

            return JsonResponse({'messages': response_messages})

        else:

            Ligne_Devis.objects.filter(devis = obj).delete()
            obj.delete()

            messages.success(request,'Le devis à été supprimé avec succès')
            
            # Extraire les messages
            response_messages = []
            for message in messages.get_messages(request):
                response_messages.append({
                    "message": message.message,
                    "tags": message.tags,
                })

            return JsonResponse({'messages': response_messages})
    
def ApiFecthDevisLigne(request):
    id_devis = request.GET.get('id_devis')

    liste = Ligne_Devis.objects.filter(devis=id_devis).values('id','produit','produit__designation','qty','tva','ttc', 'produit__prix_vente')
    
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def addToDevis(request, pk):
    obj = Devis.objects.get(id=pk)
    
    products = Products.objects.all()
    tva = Tva.objects.all()
    conf = GeneralSettings.objects.get()

    try:
        montant_ht = Ligne_Devis.objects.filter(devis__id=obj.id).aggregate(total=Sum('ht'))['total']
        montant_ttc = Ligne_Devis.objects.filter(devis__id=obj.id).aggregate(total=Sum('ttc'))['total']
        montant_tva = montant_ttc-montant_ht

    except:

        montant_tva = 0
        montant_ttc = 0
        montant_ht  = 0
    

    context = {
        'obj' : obj,
        'products' : products,
        'tva': tva,
        'conf' : conf,
        'montant_ht' : montant_ht,
        'montant_ttc' : montant_ttc, 
        'montant_tva' : montant_tva, 
        

    }
    return render(request, "conf_devis.html", context)

@login_required(login_url='/login/')
def addNewDevisProduct(request):
    if request.method == "POST":

        id_devis = request.POST.get('id_devis')
        produit = request.POST.get('produit')
        qty = request.POST.get('qty')
        taux = request.POST.get('taux')

        pr = Products.objects.get(id = produit)
        dev = Devis.objects.get(id = id_devis)
        tva = Tva.objects.get(id=taux)

        taux_appliquer = (int(tva.taux)/100)

        new_ligne = Ligne_Devis(
            produit = pr,
            devis = dev,
            qty = qty,
            tva = tva.taux,
            ht = pr.prix_vente * int(qty),
            ttc = (float((pr.prix_vente * int(qty))) * (1+taux_appliquer)) 

        )
        new_ligne.save()

        montant_ht = Ligne_Devis.objects.filter(devis__id=dev.id).aggregate(total=Sum('ht'))['total']
        montant_ttc = Ligne_Devis.objects.filter(devis__id=dev.id).aggregate(total=Sum('ttc'))['total']
        montant_tva = montant_ttc-montant_ht

        messages.success(request, "Produit ajouté avec succès")
        
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages,'montant_ht': montant_ht,'montant_ttc':montant_ttc,'montant_tva':montant_tva})
    
@login_required(login_url='/login/')
def addNewFactureProduct(request):
    if request.method == "POST":

        id_facture = request.POST.get('id_facture')
        produit = request.POST.get('produit')
        qty = request.POST.get('qty')
        taux = request.POST.get('taux')

        pr = Products.objects.get(id = produit)
        fac = Facture.objects.get(id = id_facture)
        tva = Tva.objects.get(id=taux)
        taux_appliquer = (int(tva.taux)/100)
        stock = Stock.objects.get(product = pr)


        if(int(stock.qty) > 0):
        
            if(fac.devis == None):

                new_ligne = Ligne_Facture(
                    produit = pr,
                    facture = fac,
                    qty = qty,
                    tva = tva.taux,
                    ht = pr.prix_vente * int(qty),
                    ttc = (float((pr.prix_vente * int(qty))) * (1+taux_appliquer)) 

                )
                new_ligne.save()

            else:
                new_ligne_facture = Ligne_Facture(
                    produit = pr,
                    facture = fac,
                    qty = qty,
                    tva = tva.taux,
                    ht = pr.prix_vente * int(qty),
                    ttc = (float((pr.prix_vente * int(qty))) * (1+taux_appliquer)) 

                )
                new_ligne_facture.save()

                new_ligne_devis = Ligne_Devis(
                    produit = pr,
                    devis = fac.devis,
                    qty = qty,
                    tva = tva.taux,
                    ht = pr.prix_vente * int(qty),
                    ttc = (float((pr.prix_vente * int(qty))) * (1+taux_appliquer)) 

                )
                new_ligne_devis.save()
            
            montant_ht = Ligne_Facture.objects.filter(facture__id=fac.id).aggregate(total=Sum('ht'))['total']
            montant_ttc = Ligne_Facture.objects.filter(facture__id=fac.id).aggregate(total=Sum('ttc'))['total']
            montant_tva = montant_ttc-montant_ht

            messages.success(request, "Produit ajouté avec succès")
            response_messages = []
            for message in messages.get_messages(request):
                response_messages.append({
                    "message": message.message,
                    "tags": message.tags,
                })

            return JsonResponse({'messages': response_messages,'montant_ht': montant_ht,'montant_ttc':montant_ttc,'montant_tva':montant_tva})

        else:
            
            messages.error(request, "Le produit n'est pas disponible dans le stock")

            response_messages = []
            for message in messages.get_messages(request):
                response_messages.append({
                    "message": message.message,
                    "tags": message.tags,
                })

            return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def deleteLigneDevis(request):
    id_ligne = request.GET.get('id_ligne')
    id_devis = request.GET.get('id_devis')

    Ligne_Devis.objects.get(id = id_ligne).delete()

    try:

        montant_ht = Ligne_Devis.objects.filter(devis__id=id_devis).aggregate(total=Sum('ht'))['total']
        montant_ttc = Ligne_Devis.objects.filter(devis__id=id_devis).aggregate(total=Sum('ttc'))['total']
        montant_tva = montant_ttc-montant_ht

    except:
        montant_tva = 0
        montant_ttc = 0
        montant_ht  = 0
        
    messages.success(request, "Le produit à été supprimer du devis")

    response_messages = []
    for message in messages.get_messages(request):
        response_messages.append({
            "message": message.message,
            "tags": message.tags,
        })
    return JsonResponse({'messages' : response_messages,'montant_ht' : montant_ht, 'montant_ttc' : montant_ttc, 'montant_tva':montant_tva})

@login_required(login_url='/login/')
def deleteLigneFacture(request):
    id_ligne = request.GET.get('id_ligne')
    id_facture = request.GET.get('id_facture')

    Ligne_Facture.objects.get(id = id_ligne).delete()

    try:

        montant_ht = Ligne_Facture.objects.filter(facture__id=id_facture).aggregate(total=Sum('ht'))['total']
        montant_ttc = Ligne_Facture.objects.filter(facture__id=id_facture).aggregate(total=Sum('ttc'))['total']
        montant_tva = montant_ttc-montant_ht

    except:

        montant_tva = 0
        montant_ttc = 0
        montant_ht  = 0
        
    messages.success(request, "Le produit à été supprimer de la facture")

    response_messages = []
    for message in messages.get_messages(request):
        response_messages.append({
            "message": message.message,
            "tags": message.tags,
        })
    return JsonResponse({'messages' : response_messages,'montant_ht' : montant_ht, 'montant_ttc' : montant_ttc, 'montant_tva':montant_tva})

@login_required(login_url='/login/')
def GenFactureFromDevis(request, pk):
    obj = Devis.objects.get(id = pk)

    obj.etat = "ter"
    obj.save()

    new_facture = Facture(
        user = request.user,
        devis = obj,
        client = obj.client,
        mode_paiement = obj.mode_paiement,
        delai_paiement = obj.delai_paiement,
        etat = "bro",
    )

    new_facture.save()

    lignes_devis = Ligne_Devis.objects.filter(devis__id = obj.id)

    for ligne in lignes_devis:
        new_ligne_facture = Ligne_Facture(
            facture = new_facture,
            produit = ligne.produit,
            qty = ligne.qty,
            ht = ligne.ht,
            tva = ligne.tva,
            ttc = ligne.ttc
        )
        new_ligne_facture.save()

    messages.success(request,'La facture à été crée avec succès')

    return redirect('commercial:detailFacture', new_facture.id)

def updateFactureDetails(request,pk):
    pass

@login_required(login_url='/login/')
def detailFacture(request, pk):

    obj = Facture.objects.get(id = pk)
    company = Infos_Entreprise.objects.get()
    conf = GeneralSettings.objects.get()
    items = Ligne_Facture.objects.filter(facture = obj)
    paiements = PaiementClient.objects.filter(facture = obj)
    

    montant_ht = Ligne_Facture.objects.filter(facture=obj).aggregate(total=Sum('ht'))['total']
    montant_ttc = Ligne_Facture.objects.filter(facture=obj).aggregate(total=Sum('ttc'))['total']
    montant_tva = montant_ttc-montant_ht

    try:
        montant_paye = PaiementClient.objects.filter(facture = obj).aggregate(total=Sum('montant_paiement'))['total']
        montant_restant = montant_ttc - montant_paye
    except:
        montant_restant = 0

    context = {
        'obj' : obj,
        'company' : company,
        'conf' : conf,
        'items' : items,
        'paiements' : paiements,
        'montant_ht' : montant_ht,
        'montant_ttc' : montant_ttc,
        'montant_tva' : montant_tva,
        'montant_restant' : montant_restant,
    }
    return render(request, 'details_facture.html', context)

@login_required(login_url='/login/')
def page_liste_facture(request):
    
    return render(request,'liste_des_factures.html')

@login_required(login_url='/login/')
def add_facture(request):
    form = CreateNewFacture()
    if request.method == "POST":
        form = CreateNewFacture(request.POST)
        if form.is_valid():

            date_facturation = form.cleaned_data.get('date_facturation')
            observation = form.cleaned_data.get('observation')
            client = form.cleaned_data.get('client')
            mode_paiement = form.cleaned_data.get('mode_paiement')
            delai_paiement = form.cleaned_data.get('delai_paiement')
            
            new_facture = Facture(
                user = request.user,
                etat = "bro",
                date_facturation = date_facturation,
                client = client,
                mode_paiement = mode_paiement,
                delai_paiement = delai_paiement,
                observation = observation
            )

            new_facture.save()

            messages.success(request, "Les informations de la facture ont été sauvegarder")
            return redirect('commercial:config_facture', new_facture.id )
        
        else:

            messages.error(request,'Une erreur est survenue.')
            return redirect('commercial:add_facture')
        
    else:
        context = {
            'form' : form,
        }


        return render(request, "add_facture.html", context)

@login_required(login_url='/login/')
def liste_Facture(request):

    liste = Facture.objects.all().values('id','created_at','client__designation','client','number','date_facturation','devis__number','etat')

     # Convertir la valeur du champ type_profile en son label
    for fac in liste:
        fac_instance = Facture.objects.get(id=fac['id'])
        fac['etat_label'] = fac_instance.get_etat_display()

    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def config_facture(request, pk):
    obj = Facture.objects.get(id = pk)
    conf = GeneralSettings.objects.get()
    clients = Clients.objects.all()
    products = Products.objects.all()
    tva = Tva.objects.all()
    try:

        montant_ht = Ligne_Facture.objects.filter(facture__id=obj.id).aggregate(total=Sum('ht'))['total']
        montant_ttc = Ligne_Facture.objects.filter(facture__id=obj.id).aggregate(total=Sum('ttc'))['total']
        montant_tva = montant_ttc-montant_ht

    except:

        montant_tva = 0
        montant_ttc = 0
        montant_ht  = 0

    context = {
        'obj' : obj,
        'conf' : conf,
        'montant_ht' : montant_ht,
        'montant_ttc' : montant_ttc, 
        'montant_tva' : montant_tva,
        'clients' : clients,
        'products' : products,
        'tva': tva,
    }

    return render(request,'config_facture.html', context)

@login_required(login_url='/login/')
def ApiFetchFactureItem(request):

    id_facture = request.GET.get('id_facture')

    liste = Ligne_Facture.objects.filter(facture=id_facture).values('id','produit','produit__designation','qty','tva','ttc', 'produit__prix_vente')
    
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def ApiUpdateFacture(request):
    
    if request.method == "GET":
        date_facturation = request.GET.get('new_date_facturation')
        delai_paiement = request.GET.get('new_delai_paiement')
        id_client = request.GET.get('new_client')
        mode_paiement = request.GET.get('new_mode_paiement')
        observation = request.GET.get('observation')

        id_facture = request.GET.get('id_facture')


        fact = Facture.objects.get(id = id_facture)
        client = Clients.objects.get(id = id_client)

        fact.date_facturation = date_facturation
        fact.delai_paiement = delai_paiement
        fact.client = client
        fact.mode_paiement = mode_paiement
        fact.observation = observation

        fact.save()

        messages.success(request, "Les information de la facture ont été mis à jours avec succès")

        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
@transaction.atomic
def valideInvoice(request):
    if request.method == "GET":
        id_facture = request.GET.get('id_facture')
        obj = Facture.objects.get(id = id_facture)

        obj.etat = "ter"
        obj.save()

        ligne_facture = Ligne_Facture.objects.filter(facture = obj)

        for i in ligne_facture:

            new_mouvement = Mouvements_produit(
                user = request.user,
                produit = i.produit,
                qty = i.qty,
                type_mouvement = "sor",
                description = f"Sortie de stock Facture N° {obj.number}",
            )
            new_mouvement.save()

        messages.success(request, "La facture à été validé ")
        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def deleteFacture(request):
    if request.method == "GET":
        id_fact = request.GET.get('id_lign')

        fac = Facture.objects.get(id = id_fact)

        fac.delete()
        messages.success(request,"La facture à été supprimer avec succès")
        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def FactureAvoirePage(request):
    factures = Facture.objects.filter(etat="ter")
    conf = GeneralSettings.objects.get()

    context = {
        'factures' : factures,
        'conf' : conf,
    }
    return render(request,"liste_facture_avoir.html", context)

@login_required(login_url='/login/')
def APIGetFactureAvoir(request):

    liste = Facture_Avoir.objects.all().values('id','number','ref_facture','ref_facture__number','ref_facture__client__designation','created_at','etat')
    for fac in liste:
        fac_instance = Facture_Avoir.objects.get(id=fac['id'])
        fac['etat_label'] = fac_instance.get_etat_display()
        fac['created_at'] = fac['created_at'].strftime('%Y-%m-%d')

    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def CreateAvoir(request):
    id_facture = request.POST.get('id_facture')
    motif_avoir = request.POST.get('motif_avoir')

    obj = Facture.objects.get(id=id_facture)
    ligne_obj = Ligne_Facture.objects.filter(facture = obj)

    new_avoir = Facture_Avoir(
        user = request.user,
        ref_facture = obj,
        motifs = motif_avoir,
        etat = "bro",
    )

    new_avoir.save()

    for lg in ligne_obj:
        new_ligne_avoir = LigneFactureAvoir(
            ref_facture_avoir =  new_avoir,
            produit = lg.produit,
            qty = lg.qty,
            ht = lg.ht,
            tva = lg.tva,
            ttc = lg.ttc,
        )

        new_ligne_avoir.save()
    
    messages.success(request, "La facture d'avoir à été crée avec succès")

    response_messages = []
    for message in messages.get_messages(request):
        response_messages.append({
            "message": message.message,
            "tags": message.tags,
        })

    return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def deleteFactureAvoir(request):
    if request.method == "GET":
        
        id_avoir = request.GET.get('id_avoir')
        obj = Facture_Avoir.objects.get(id = id_avoir)
        LigneFactureAvoir.objects.filter(ref_facture_avoir = obj).delete()
        obj.delete()

        messages.success(request, "La facture d'avoir à été supprimé avec succès")

        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
            "message": message.message,
            "tags": message.tags,
        })
            
        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def AvoirConf(request, pk):

    obj = Facture_Avoir.objects.get(id = pk)
    conf = GeneralSettings.objects.get()
    products = Products.objects.all()
    tva = Tva.objects.all()

    try:
        montant_ht = LigneFactureAvoir.objects.filter(ref_facture_avoir__id=obj.id).aggregate(total=Sum('ht'))['total']
        montant_ttc = LigneFactureAvoir.objects.filter(ref_facture_avoir__id=obj.id).aggregate(total=Sum('ttc'))['total']
        montant_tva = montant_ttc-montant_ht
    except:

        montant_tva = 0
        montant_ttc = 0
        montant_ht  = 0

    context = {
        'obj' : obj,
        'conf' : conf,
        'products' : products,
        'tva' : tva,
        'montant_tva': montant_tva,
        'montant_ttc': montant_ttc,
        'montant_ht': montant_ht,
    }
    return render(request,'config_facture_avoir.html', context)

@login_required(login_url='/login/')
def ApiFetchFactureAvoirItem(request):
    if request.method =="GET":
        id_facture_avoir = request.GET.get('id_facture_avoir')
    
        ligne_facture_avoir = LigneFactureAvoir.objects.filter(ref_facture_avoir = id_facture_avoir).values('id','produit','produit__designation','qty','tva','ttc', 'produit__prix_vente')
        return JsonResponse(list(ligne_facture_avoir), safe=False)

@login_required(login_url='/login/')
def validateFactureAvoir(request):
    pass

@login_required(login_url='/login/')
def ApiFetchLigneAvoirDetails(request):
    if request.method == 'GET':
        id_ligne = request.GET.get('id_ligne')
        obj = LigneFactureAvoir.objects.filter(id = id_ligne).values('id','produit__designation', 'qty')

        return JsonResponse(list(obj), safe=False)

@login_required(login_url='/login/')
@transaction.atomic
def ApiUpdateLigneFactureAvoir(request):
    if request.method == 'POST':

        lign_facture_avoir = request.POST.get('lign_facture_avoir')
        qty_retour = request.POST.get('qty_retour')
        motif_retour = request.POST.get('motif_retour')
        if_reintegre = request.POST.get('if_reintegre')

        avoir = LigneFactureAvoir.objects.get(id = lign_facture_avoir)
        taux_appliquer = (int(avoir.tva)/100)
        
        if if_reintegre == "non":

            avoir.qty = int(avoir.qty) - int(qty_retour)
            avoir.save()

            avoir.ht = int(avoir.qty) * avoir.produit.prix_vente
            avoir.ttc = (float((avoir.produit.prix_vente * int(avoir.qty))) * (1+taux_appliquer)) 

            avoir.save()

            new_mouvement = Mouvements_produit(
                user = request.user,
                produit = avoir.produit,
                type_mouvement = "ent",
                qty = qty_retour,
                description = motif_retour,
            )
            new_mouvement.save()

            new_retour_produit = RetourProduit(
                user = request.user,
                product = avoir.produit,
                ref = lign_facture_avoir,
                observation = motif_retour,
            )
            new_retour_produit.save()

            messages.success(request, "L'opération à été effectuer avec succès")

            response_messages = []
            for message in messages.get_messages(request):
                response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })
                
            return JsonResponse({'messages': response_messages})
        
        else:

            avoir.qty = int(avoir.qty) - int(qty_retour)
            avoir.save()

            avoir.ht = int(avoir.qty) * avoir.produit.prix_vente
            avoir.ttc = (float((avoir.produit.prix_vente * int(avoir.qty))) * (1+taux_appliquer)) 

            avoir.save()

            new_mouvement = Mouvements_produit(
                user = request.user,
                produit = avoir.produit,
                type_mouvement = "ent",
                qty = qty_retour,
                description = motif_retour,
            )
            new_mouvement.save()

            new_retour_produit = RetourProduit(
                user = request.user,
                product = avoir.produit,
                ref = lign_facture_avoir,
                observation = motif_retour,
            )
            new_retour_produit.save()
            
            obj = Stock.objects.get(produit = avoir.produit)

            new_stock = Stock(
                user = request.user,
                product = avoir.produit,
                qty = int(obj.qty) + int(qty_retour)
            )
            new_stock.save()

            messages.success(request, "L'opération à été effectuer avec succès")

            response_messages = []
            for message in messages.get_messages(request):
                response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })
                
            return JsonResponse({'messages': response_messages})


        
   
#################### GESTION DES DEVIS ET FACTURES ##############################################

############## GESTION DES UTILISATEURS #############################################

@login_required(login_url='/login/')
def PageListeUtilisateur(request):
    return render(request,'liste_des_utilisateurs.html')

@login_required(login_url='/login/')
def ListeDeUtilisateurs(request):
    liste = Profile.objects.all().values('id','user__id','user__username','nom','prenom','type_profile','user__is_active','user__email')

    # Convertir la valeur du champ type_profile en son label
    for profile in liste:
        profile_instance = Profile.objects.get(id=profile['id'])
        profile['type_profile_label'] = profile_instance.get_type_profile_display()
        
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def addNewUserProfile(request):
    if request.method == "POST":
        username = request.POST.get('new_username')
        email = request.POST.get('new_email')
        password = request.POST.get('new_mot_passe')

        nom = request.POST.get('new_nom')
        prenom = request.POST.get('new_prenom')

        if not Profile.objects.filter(user__username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)

            prof = Profile.objects.get(user=user)

            prof.nom = nom
            prof.prenom = prenom

            prof.save()
                

            messages.success(request, "Un nouvelle utilisateur à été créer !")
        else:
            messages.error(request, "Le nom d'utilisateur existe déja, veuillez en choisir un autre !")

        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def GetProfileInfo(request):
    id_profile = request.GET.get('id_profile')

    profile = Profile.objects.filter(id=id_profile).values('id','user__id','nom','prenom','user__username','etat','user__is_active','user__email')

    return JsonResponse(list(profile), safe=False)

@login_required(login_url='/login/')
@transaction.atomic
def updateProfile(request):

    if request.method == "POST":
        
        id = request.POST.get('id')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')

        profile = Profile.objects.get(id=id)

        profile.nom = nom
        profile.prenom = prenom

        profile.save()

        messages.success(request, "Le profil a été modifié !")

        # Extraire les messages
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def userDetails(request, pk):
    obj = User.objects.get(id=pk)
    context = {
        'obj' : obj,
    }
    return render(request,"details_utilisateur.html", context)

@login_required(login_url='/login/')
def deleteUser(request):
    user_id = request.GET.get('id')
    obj = User.objects.get(id = user_id)
    obj.delete()
    messages.success(request, "L'utilisateur et le profile ont été supprimer avec succès !")

    response_messages = []
    for message in messages.get_messages(request):
        response_messages.append({
            "message": message.message,
            "tags": message.tags,
        })

    return JsonResponse({'messages': response_messages})

############## GESTION DES UTILISATEURS #############################################

############## GESTION DE LAS CAISSE ################################################
@login_required(login_url='/login/')
def PosDashboard(request):
    caisse = Caisse.objects.all()
    nb_vente = LigneCaisse.objects.all()
    montant_des_ventes = LigneCaisse.objects.all().aggregate(total=Sum('montant_total'))['total']
    config = GeneralSettings.objects.get()

    if montant_des_ventes == None:
        montant_des_ventes = 0

    try:
        session = SessionVente.objects.get(etat="1")
        context = {
            'caisse' : caisse,
            'nb_vente' : nb_vente,
            'session' : session,
            'montant_des_ventes' : montant_des_ventes,
            'config' : config
        }
        return render(request, 'pos-dashboard.html',context)
    
    except ObjectDoesNotExist:
        context = {
            'caisse' : caisse,
            'nb_vente' : nb_vente,
            'montant_des_ventes' : montant_des_ventes,
            'config' : config
        }
        return render(request, 'pos-dashboard.html',context)

@login_required(login_url='/login/')
@transaction.atomic
def pos(request):

    # Récupérer la dernière caisse, ou None si aucune caisse n'existe
    last_caisse = Caisse.objects.filter(etat="1").order_by('-num').first()
    last_session = SessionVente.objects.filter(etat="1").order_by('-num').first()
    product = Products.objects.all()
    config = GeneralSettings.objects.get()
    montant_session = LigneCaisse.objects.filter(session=last_session).aggregate(total=Sum('montant_total'))['total']

    if montant_session is None:
        montant_session = 0  # S'il n'y a aucune entrée correspondante, on peut renvoyer 0


    # Si aucune caisse n'existe, en créer une nouvelle
    if last_caisse is None:
        new_caisse = Caisse(
            user=request.user,
            etat="1"
        )
        new_caisse.save()
        last_caisse = new_caisse

        new_session = SessionVente(
            user = request.user,
            caisse = new_caisse,
            etat = "1"
        )

        new_session.save()
        last_session = new_session

    # Préparer le contexte avec la dernière caisse (ou la nouvelle caisse)
    context = {
        'last_caisse': last_caisse,
        'last_session' : last_session,
        'product' : product,
        'config' : config,
        'montant_session' : montant_session,
    }

    # Renvoyer la réponse avec le template 'pos.html' et le contexte
    return render(request, 'pos.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def new_session(request):
    last_session = SessionVente.objects.filter(etat="1").order_by('-num').first()
    
    lignes_caisse = LigneCaisse.objects.filter(session=last_session)
    
    for ligne in lignes_caisse:
        try:
            stock_item = Stock.objects.get(product=ligne.product)
            stock_item.qty = int(stock_item.qty) - int(ligne.qty)
            stock_item.save()

            last_session.etat = "0"
            last_session.save()

        except ObjectDoesNotExist:

            messages.error(request,"Le produit n'a pas de stock définie <br> Veuillez vérifier votre stock")
            return redirect('commercial:pos')
        
    last_caisse = Caisse.objects.filter(etat="1").order_by('-num').first()
    new_session = SessionVente(
        user = request.user,
        etat= "1",
        caisse = last_caisse
    )
    new_session.save()

    messages.success(request,'Succès ! <br> Nouvelle vente crée avec succès')
    return redirect('commercial:pos')

@login_required(login_url='/login/')
def ligneCaisse(request):
    last_session = SessionVente.objects.filter(etat="1").order_by('-num').first()
    
    liste = LigneCaisse.objects.values('product','product__designation','prix_vente','qty').filter(session = last_session).order_by('created_at')

    return JsonResponse(list(liste), safe=False) 

@login_required(login_url='/login/')
def clotureCaisse(request,pk):

    last_session = SessionVente.objects.filter(etat="1").order_by('-num').first()
    ligne_vente = LigneCaisse.objects.filter(session = last_session)

    if last_session:

        if ligne_vente:

            messages.error(request, "Veuillez valider le bon actuelle")
            return redirect('commercial:pos')
        
        last_session.delete()
        
        caisse = Caisse.objects.get(id=pk)
        caisse.etat="0"
        caisse.save()

        messages.success(request, "La caisse du jour à été cloturé avec succès")
        return redirect('commercial:pos_dashboard')
    
    else:

        caisse = Caisse.objects.get(id=pk)
        caisse.etat="0"
        caisse.save()
        messages.success(request, "La caisse du jour à été cloturé avec succès")
        return redirect('commercial:pos_dashboard')

def check_product(prod):
    return Stock.objects.filter(product=prod).exists()

@login_required(login_url='/login/')
@transaction.atomic
def add_product_to_sale(request):
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        vente_id = request.POST.get('vente_id')
        qty = request.POST.get('qty')
        
        try:

            product = Products.objects.get(id=product_id)
            vente = SessionVente.objects.get(num = vente_id)

            if not check_product(product):
                return JsonResponse({'success': False, 'message': 'Produit non disponible en stock'})

            if LigneCaisse.objects.filter(product=product, session=vente).exists():
                return JsonResponse({'success': False, 'message': 'Produit déjà présent dans la vente'})    
            
            
            ventes = LigneCaisse(
                user = request.user,
                product = product,
                prix_vente = product.prix_vente,
                session = vente,
                qty = qty,
                montant_total = int(qty)*product.prix_vente,
            )
            ventes.save()
            
            montant_session = LigneCaisse.objects.filter(session=vente).aggregate(total=Sum('montant_total'))['total']

            if montant_session is None:
                montant_session = 0  # S'il n'y a aucune entrée correspondante, on peut renvoyer 0

            
            return JsonResponse({'success': True, 'message': 'Produit ajouté à la vente', 'montant_session': montant_session,})
        
        except Products.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Produit non trouvé'})
        
    
    return JsonResponse({'success': False, 'message': 'Requête invalide'})

@login_required(login_url='/login/')
def update_product_qty(request):    
    try:

        product_id = request.POST.get('product_id')
        vente_id = request.POST.get('vente_id')
        new_qty = int(request.POST.get('qty'))

        if new_qty < 1:
            return JsonResponse({'success': False, 'message': 'La quantité doit être au moins 1.'})

        # Récupérer la ligne de vente correspondante
        ligne_vente = LigneCaisse.objects.get(session__num=vente_id, product=product_id)
        ligne_vente.qty = new_qty
        ligne_vente.montant_total = new_qty * ligne_vente.prix_vente
        ligne_vente.save()

        vente = SessionVente.objects.get(num = vente_id)
        
        montant_session = LigneCaisse.objects.filter(session=vente).aggregate(total=Sum('montant_total'))['total']

        if montant_session is None:
            montant_session = 40  # S'il n'y a aucune entrée correspondante, on peut renvoyer 0

        return JsonResponse({'success': True, 'message': 'Quantité mise à jour avec succès.','montant_session':montant_session})

    except LigneCaisse.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Produit introuvable dans la vente.'})
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Quantité non valide.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required(login_url='/login/')
def listBons(request):
    liste = SessionVente.objects.all()
    config = GeneralSettings.objects.get()
    
    # Calculer le montant total pour chaque session
    session_data = []

    for session in liste:
        montant_session =   LigneCaisse.objects.filter(session=session).aggregate(total=Sum('montant_total'))['total'] or 0
        session_data.append({
            'session': session,
            'montant_session': montant_session
        })

    context = {
        'session_data': session_data,
        'config' : config,
    }

    return render(request,'liste_des_bons.html', context)

@login_required(login_url='/login/')
def listDesVente(request):
    liste = LigneCaisse.objects.all()
    config = GeneralSettings.objects.get()
    context = {
        'config' : config,
        'liste' : liste
    }
    return render(request,'liste_des_ventes.html', context)

@login_required(login_url='/login/')
@csrf_exempt
def remove_product_from_sale(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            vente_id = request.POST.get('vente_id')

            ligne_vente = LigneCaisse.objects.get(product=product_id, session__num=vente_id)
            
            if ligne_vente:

                ligne_vente.delete()
                
                # Recalculer le montant total de la session
                montant_session = LigneCaisse.objects.filter(session_id=vente_id).aggregate(total=Sum('montant_total'))['total'] or 0
                
                return JsonResponse({
                    'success': True,
                    'montant_session': montant_session,
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Le produit n\'existe pas dans cette vente.',
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e),
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Méthode de requête non autorisée.',
        })

@login_required(login_url='/login/')
def list_caisse(request):

    liste = Caisse.objects.all()
    config = GeneralSettings.objects.get()

    nb_vente = []
    
    for caisse in liste:
        sessions = SessionVente.objects.filter(caisse=caisse)
        montant_total = LigneCaisse.objects.filter(session__in=sessions).aggregate(total=Sum('montant_total'))['total'] or 0

        nb_vente.append({
            'caisse': caisse,
            'nombre_vente': sessions.count(),
            'montant_total': montant_total,
        })
        

    context = {
        'nb_vente' : nb_vente,
        'config' : config,
    }
    return render(request, 'liste_des_caisses.html', context)

@login_required(login_url='/login/')
def liste_session_caisse(request):

    id_caisse = request.GET.get('id_caisse')

    caisse = Caisse.objects.get(num = id_caisse)

    sessions = SessionVente.objects.filter(caisse = caisse).values('num','created_at','user__username')

    sessions_with_total = []

    for session in sessions:
        montant_total = LigneCaisse.objects.filter(session__num=session['num']).aggregate(total=Sum('montant_total'))['total'] or 0
        session['montant_total'] = montant_total
        sessions_with_total.append(session)

    return JsonResponse(list(sessions_with_total), safe=False)


############## GESTION DE LA CAISSE ################################################

############## GESTION DES CLIENTS #################################################
@login_required(login_url='/login/')
@transaction.atomic
def client_view(request):
    if request.method == 'POST':
        form = ClientAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Les information ont été enregistrer avec succès")

            return redirect('commercial:client-list')
        
    form = ClientAddForm()

    return render(request, 'add-client.html', {'form': form})

@login_required(login_url='/login/')
def client_liste(request):
    list = Clients.objects.all()

    context = {
        'list' : list
    }

    return render(request, 'liste_des_clients.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def client_update(request, pk):
    obj = Clients.objects.get(id=pk)
    form = ClientAddForm(instance=obj)
    if request.method == 'POST':
        form = ClientAddForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Les informations ont été modifier avec succès')
            return redirect('commercial:client_update', pk)
        else:
            messages.error(request,'Une erreur c\'produit lors du traitement des informations')
    
    context = {
        'form' : form
    }
    return render(request,'update_client.html', context)

@login_required(login_url='/login/')
def list_prospect(request):
    list = Prospects.objects.all()
    context = {
        'list' : list
    }
    return render(request, "list_prospect.html", context)

@login_required(login_url='/login/')
def add_prospects(request):
    form = ProspectForm()
    if request.method == 'POST':
        form = ProspectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insérer avec succès')
            return redirect('commercial:list_prospect')
    else:
        context = {
            'form' : form
        }
        return render(request, "ajouter_prospect.html", context)

@login_required(login_url='/login/')
def clientDetails(request, pk):
    obj = Clients.objects.get(id = pk)
    devis = Devis.objects.filter(client = obj)
    facture = Facture.objects.filter(client = obj)
    
    montant = Ligne_Facture.objects.filter(facture__in = facture).aggregate(total=Sum('ht'))['total']
    paye = PaiementClient.objects.filter(facture__in = facture).aggregate(total=Sum('montant_paiement'))['total']
    
    if paye == None:
        impaye = montant
    else:
        if montant == paye:
            impaye = 0
        else:
            impaye = montant - paye



    conf = GeneralSettings.objects.get()

    context = {
        'conf' : conf,
        'obj' : obj,
        'devis' : devis,
        'facture' : facture,
        'montant' : montant,
        'paye' : paye,
        'impaye' :  impaye,
    }

    return render(request, 'details_du_client.html', context)

############## GESTION DES CLIENTS #################################################

############## GESTION OPPORTUNITE #################################################
def liste_opportunite(request):
    list = Opportunites.objects.all()
    context = {
        'list': list
    }
    return render(request, "list_opportunite.html", context)

def add_opportunite(request):
    form = OpportuniteForm()
    if request.method == "POST":
        form = OpportuniteForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Les informations ont été enregistrer avec succès')
            return redirect('commercial:liste_opportunite')
    else:

        context = {
            'form' : form
        }
        return render(request, 'ajouter_opportunite.html', context)
############## GESTION OPPORTUNITES ################################################

############## GESTION DES PRODUITS ################################################
@login_required(login_url='/login/')
def product_liste(request):
    try:
        config = GeneralSettings.objects.latest('created_at')
    except ObjectDoesNotExist:
        config = None

    list = Products.objects.all()

    context = {
        'list' : list,
        'config' : config,
    }

    return render(request, 'liste-des-produits.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def add_product(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():

            new_product = form.save()

            Stock.objects.create(
                product = new_product,
                qty = 0
            )

            return redirect('commercial:product-liste')
    else:

        form = ProductAddForm()
        context = {
            'form' : form
        }

        return render(request ,'ajouter-un-produit.html', context)

def details_produit(request, pk):

    try:
        config = GeneralSettings.objects.latest('created_at')
    except ObjectDoesNotExist:
        config = None

    obj = Products.objects.get(id = pk)

    context = {
        'obj' : obj,
        'config' : config
    }
    return render(request, 'details_produit.html', context)

@transaction.atomic
def update_produit(request, pk):
    obj = Products.objects.get(id=pk)
    form = ProductAddForm(instance=obj)

    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Les informations ont été enregistrer avec succès")
            return redirect('commercial:details-produit',pk)
        else:
            messages.error(request,"Une erreur c'est produite lors du traitement de la requête.")
            return redirect('commercial:update_produit',pk)
        
    context = {
        'form' : form
    }

    return render(request, 'update_product.html', context)

@login_required(login_url='/login/')
def delete_product(request, pk):
    prod = Products.objects.get(id=pk)
    prod.delete()
    messages.success(request,"Le produit à été supprimé avec succès")
    return redirect('commercial:product-liste')

@login_required(login_url='/login/')
def PageListeService(request):
    categorie = Categorie_produit.objects.all()
    print(categorie)
    context = {
        'categorie' : categorie,
    }
    return render(request,"liste_des_services.html", context)

@login_required(login_url='/login/')
def ApiLoadService(request):
    liste = Products.objects.filter(type_produit = "srv").values('designation','prix_vente','categorie','created_at','ref','disponibilite')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def AddNewService(request):
    if request.method == "POST":
        new_service_name = request.POST.get('new_service_name')
        new_service_ref = request.POST.get('new_service_ref')
        new_service_tarif = request.POST.get('new_service_tarif')
        type_tarification = request.POST.get('type_tarification')
        categorie = request.POST.get('categorie')
        dispo = request.POST.get('dispo')
        description = request.POST.get('description'),

        obj_categorie = Categorie_produit.objects.get(id = dispo)

        new_service = Products(
            user = request.user,
            designation = new_service_name,
            ref = new_service_ref,
            prix_vente = new_service_tarif,
            type_tarifcation = type_tarification,
            categorie = obj_categorie,
            disponibilite = dispo,
            description = description,
        )
        new_service.save()
        messages.success(request, "Les informations ont été enregistrer avec succès")
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})


############## GESTION DES PRODUITS ################################################

############## CATEGORIE DES PRODUITS ##############################################
@login_required(login_url='/login/')
def list_categorie(request):
    list = Categorie_produit.objects.all()
    context = {
        'list' : list
    }
    return render(request, 'liste_categorie_produit.html', context)

@login_required(login_url='/login/')
def add_categorie(request):
    form = ProductCategoriForm()
    if request.method == 'POST':
        form = ProductCategoriForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('commercial:categorie_list')
    else:

        context = {
            'form' : form,
        }

        return render(request, 'ajouter_categorie_produit.html', context)

@login_required(login_url='/login/')
def update_categorie(request, pk):
    obj = Categorie_produit.objects.get(id=pk)

    form = ProductCategoriForm(instance=obj)

    if request.method == 'POST':
        form = ProductCategoriForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            return redirect('commercial:categorie_list')
        
    else:

        context = {
            'form' : form
        }
        return render(request, 'update_categorie_produit.html', context)

@login_required(login_url='/login/')
def categorieProduit(request):
    categories = Categorie_produit.objects.annotate(nombre_produits=Count('products'))
    context = {
        'categories' : categories
    }
    return render(request, 'produit_par_categorie.html', context)

@login_required(login_url='/login/')
def ApiFetchProductCat(request):
    id_cat = request.GET.get('id_cat')
    categorie = Categorie_produit.objects.get(id=id_cat)

    liste = Products.objects.filter(categorie = categorie).values('id','designation','ref','code_barre')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def ApiFetchProductDetails(request):
    if request.method =="GET":
        id_product = request.GET.get('id_product')

        product = Products.objects.filter(id = id_product).values('id','designation','categorie').first()
        categories = list(Categorie_produit.objects.all().values('id','label'))

        data = {
            'product' : product,
            'categories' : categories,
        }

        return JsonResponse(data, safe=False)

        

############## CATEGORE DES PRODUITS ###############################################

############## STOCK DES PRODUITS ##################################################
@login_required(login_url='/login/')
def etat_stock(request):
    list = Stock.objects.all()
    produits = Products.objects.all()
    context = {
        'list':list,
        'produits' : produits,
    }
    return render(request,'etat_du_stock.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def nouvelle_entree_stock(request):

    if request.method == "POST":
        
        type_mvmt = request.POST.get('type_mouvement')
        qty = request.POST.get('qty')
        product_id = request.POST.get('product')
        selected_product = Products.objects.get(id=product_id)
        description = request.POST.get('description')

        try:
            stock = Stock.objects.get(product = selected_product)
            stock.qty = str(int(stock.qty) + int(qty))            
            stock.save()

            new_mouvement = Mouvements_produit(
                user = request.user,
                produit = selected_product,
                type_mouvement = type_mvmt,
                description = description,
                qty = qty,
            )
            new_mouvement.save()    
            messages.success(request, "Enregistrer avec succès")
            return redirect('commercial:etat_stock')
            
        except ObjectDoesNotExist:
            new_mouvement = Mouvements_produit(
                user = request.user,
                produit = selected_product,
                type_mouvement = type_mvmt,
                description = description,
                qty = qty,
            )
            new_stock = Stock(
                product = selected_product,
                qty = qty,
            )
            new_stock.save()
            new_mouvement.save()
            messages.success(request, "Enregistrer avec succès")
            return redirect('commercial:etat_stock')

@login_required(login_url='/login/')
def PageMouvementListe(request):
    return render(request,'mouvements_produits.html')

@login_required(login_url='/login/')
def ApiGetMouvItem(request):
    liste = Mouvements_produit.objects.all().values('id','type_mouvement','produit__designation','produit__ref','produit__code_barre','qty','created_at')
    for p in liste:
        p_instance = Mouvements_produit.objects.get(id=p['id'])
        p['type_mouvement_label'] = p_instance.get_type_mouvement_display()

    return JsonResponse(list(liste), safe=False)

@login_required(login_url='/login/')
def DeleteMouvementLine(request):
    if request.method == "GET":
        id_mouv_lign = request.GET.get('mouvLineId')
        obj = Mouvements_produit.objects.get(id = id_mouv_lign)
        obj.delete()

        messages.success(request,"Le mouvement du produit à été supprimer avec succès")
        response_messages = []
        for message in messages.get_messages(request):
            response_messages.append({
                "message": message.message,
                "tags": message.tags,
            })

        return JsonResponse({'messages': response_messages})

@login_required(login_url='/login/')
def ApiDetailsMouvement(request):
    if request.method == "GET":
        id_ligne_mouv = request.GET.get('id_ligne_mouv')

        # Récupérer l'objet spécifique avec le type de mouvement
        obj = Mouvements_produit.objects.filter(id=id_ligne_mouv).first()
        
        if obj:
            # Créer un dictionnaire avec les détails et le label du type de mouvement
            data = {
                'user' : obj.user.username,
                'id': obj.id,
                'qty': obj.qty,
                'produit_designation': obj.produit.designation,
                'description': obj.description,
                'type_mouvement_label': obj.get_type_mouvement_display(),  # Obtenir le label du champ type_mouvement
                'created_at': obj.created_at
            }
            return JsonResponse(data, safe=False)

############## STOCK DES PRODUITS ##################################################

############## GESTION DES FOURNISSEURS ############################################
@login_required(login_url='/login/')
def liste_fournisseur(request):
    list = Fournisseurs.objects.all()
    context = {
        'list': list
    }
    return render(request,'liste_des_fournisseurs.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def nouveau_fournisseur(request):
    form = FournisseurAddForm()
    if request.method == 'POST':
        form = FournisseurAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Les informations ont été enregistrer avec succès')
            return redirect('commercial:liste_fournisseur')
        
        else:
            messages.error(request,'Une erreur c\'est produit lors du traitement des données')
            return redirect('commercial:nouveau_fournisseur')

    context= {
        'form' : form
    }
    return render(request,'add_fournisseur.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def update_fournisseur(request, pk):
    obj = Fournisseurs.objects.get(id=pk)
    form = FournisseurAddForm(instance=obj)
    if request.method == 'POST':
        form = FournisseurAddForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Les informations ont été modifier avec succès')
            return redirect('commercial:update_fournisseur', pk)
        else:
            messages.error(request,"Une erreur c'est produite lors du traitement de la requête.")
            return redirect('commercial:update_fournisseur', pk)
    
    context = {
        'form' : form
    }
    return render(request, 'update_fournisseur.html', context)

def detail_fournisseur(request):
    pass

def delete_fournisseur(request):
    pass
############## GESTION DES FOURNISSEURS ############################################

         
############## GESTION DES NOTES ###################################################
@login_required(login_url='/login/')
def liste_notes(request):
    list = Notes.objects.all()
    context = {
        'list' : list
    }
    return render(request, 'liste-des-notes.html', context)

@login_required(login_url='/login/')
@transaction.atomic
def add_note(request):
    form = NotesForm()
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():

            note = Notes(
                user = request.user,
                text = form.cleaned_data['text']
            )

            note.save()
            messages.success(request, 'La note est enregistrer avec succès')
        
            return redirect('commercial:mes_notes')
        
        else:
            messages.error(request, 'La note est enregistrer avec succès')

    context={
        'form' : form
    }
    return render(request,'ajouter_note.html', context)
############## GESTION DES NOTES ###################################################

############## GESTION DES RAPPELS #################################################
class RappelCreateView(BSModalCreateView):
    template_name = 'modals/create_rappel.html'
    form_class = Rappels
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('commercial:liste_rappele')

def ListeDesRappels(request):
    list = Rappels.objects.all()
    prospect = Prospects.objects.all()
    context = {
        'list':list,
        'prospect' : prospect,
    }
    return render(request, 'liste_des_rappels.html', context)

def nouveau_rappele(request):

    if request.method == "POST":

        description = request.POST.get('description')
        date_rappel = request.POST.get('date_rappel')
        heur_rappel = request.POST.get('heur_rappel')
        priority = request.POST.get('priority')
        type_rappel = request.POST.get('type_rappel')

        prospect = request.POST.get('prospect')
        selected_prospect = Prospects.objects.get(id=prospect)

        new_rappel = Rappels(
            user = request.user,
            prospect = selected_prospect,
            observation = description,
            date_rappel = date_rappel,
            time = heur_rappel,
            priority = priority,
            type_rappel = type_rappel,
            etat = 'enc',
        )

        new_rappel.save()
        messages.success(request,"Les informtions ont été enregistrer avec succès")

        return redirect('commercial:liste_rappele')

############## GESTION DES RAPPELS #################################################

def configuration(request):
    conf= GeneralSettings.objects.get()
    try:
        obj = GeneralSettings.objects.latest('created_at')
        form = ParamGenForm(instance=obj)
        if request.method == 'POST':
            form = ParamGenForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request,"Les informations ont été enregistrer avec succès")
                return redirect('commercial:configuration')
            
            else:
                messages.error(request,"Les informations ont été enregistrer avec succès")
                return redirect('commercial:configuration')
        
        context= {
            'form' : form,
            'conf'  : conf,
        }

        return render(request, 'configuration.html', context)   

    except ObjectDoesNotExist:
    
        form = ParamGenForm()
        if request.method == 'POST':
            form = ParamGenForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Les informations ont été enregistrer avec succès")
                return redirect('commercial:configuration')
            else:
                messages.error(request, "Une erreu c'est produite lors du traitement de la requete")
                return redirect('commercial:configuration')
        context= {
            'form' : form,
            'conf'  : conf,
        }

        return render(request, 'configuration.html', context)




