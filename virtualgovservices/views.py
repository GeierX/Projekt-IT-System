from signxml import XMLSigner
from lxml import etree
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import signxml
import base64
from .models import Buerger, Hundeanmeldung, Dokument, Verfahren, Beamter, Wohnsitzanmeldung
from django.contrib import messages
from .forms import BuergerDatenForm, HundeanmeldungForm, WohnsitzanmeldungForm, BescheidForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count



def landingpage(request): #Germann
    return render(request, "virtualgovservices/landingpage.html")


def login(request): #Germann
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main')
            # # Bestimme die Rolle des eingeloggten Benutzers basierend auf deinen Modellen
            # if hasattr(user, 'beamter'):  # Prüft, ob es ein Beamter ist
            #     return redirect('main_beamter')  # Leitet zum Template für Beamte weiter
            # elif hasattr(user, 'buerger'):  # Prüft, ob es ein Bürger ist
            #     return redirect('main')  # Leitet zum Template für Bürger weiter
        else:
            messages.error(
                request, 'Ungültiger Benutzername oder falsches Passwort!')
            return redirect(login)

    else:
        return render(request, "virtualgovservices/login.html")


def signup(request): #Germann
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Benutzername bereits vergeben!')
            return redirect(signup)
        else:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()

            user_login = auth.authenticate(
                username=username, password=password)
            auth.login(request, user_login)

            # user_model = User.objects.get(username=username)
            new_buerger = Buerger.objects.create(
                user=user)
            new_buerger.save()
            messages.success(request, 'Benutzer erfolgreich angelegt. Bitte vervollständigen Sie Ihre Daten, damit diese bei Anträge übernommen werden können.')
            return redirect("settings")
    else:
        return render(request, "virtualgovservices/signup.html")


@login_required(login_url='landingpage') #Germann
def logout(request):
    auth.logout(request)
    messages.success(request, 'Erfolgreich abgemeldet!')
    return redirect('landingpage')


@login_required(login_url='landingpage')
def main(request):
    user = request.user
    buerger = Buerger.objects.filter(user=user).first()
    beamter = Beamter.objects.filter(user=user).first()

    if buerger:
        verfahren_liste = Verfahren.objects.filter(antragssteller=user)

        context = {
            'loggedin_user': buerger,
            'verfahren_liste': verfahren_liste,
        }
        return render(request, 'virtualgovservices/mainpage.html', context)

    elif beamter:
        verfahren_liste = Verfahren.objects.filter(verantwortlicher=beamter)

        for verfahren in verfahren_liste:
            buerger = get_object_or_404(Buerger, user=verfahren.antragssteller)
            verfahren.buerger_anrede = buerger.anrede
            verfahren.buerger_vorname = buerger.vorname
            verfahren.buerger_nachname = buerger.nachname
            verfahren.buerger_telefonnummer = buerger.telefonnummer
            verfahren.buerger_email = buerger.email

        context = {
            'loggedin_user': beamter,
            'verfahren_liste': verfahren_liste,
        }

        return render(request, 'virtualgovservices/beamte_mainpage.html', context)


@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Buerger.objects.get(user=user_object)
    loggedin_user = Buerger.objects.get(user=request.user)
    # user_antrag =

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'loggedin_user': loggedin_user
    }
    return render(request, 'virtualgovservices/profil.html', context)


@login_required(login_url='landing_page') #Germann
def profile_settings(request):
    if Buerger.objects.filter(user=request.user).exists():
        loggedin_user = Buerger.objects.get(user=request.user)

        if request.method == 'POST':

            if request.FILES.get('profileimg') == None:
                profileimg = loggedin_user.profileimg
                loggedin_user.profileimg = profileimg

            if request.FILES.get('profileimg') != None:
                profileimg = request.FILES.get('profileimg')
                loggedin_user.profileimg = profileimg
            
            anrede = request.POST['anrede']
            vorname = request.POST['vorname']
            nachname = request.POST['nachname']
            strasse = request.POST['strasse']
            postleitzahl = request.POST['postleitzahl']
            ort = request.POST['ort']
            telefonnummer = request.POST['telefonnummer']
            email = request.POST['email']
            geburtsdatum = request.POST['geburtsdatum']

            loggedin_user.anrede = anrede
            loggedin_user.vorname = vorname
            loggedin_user.nachname = nachname
            loggedin_user.strasse = strasse
            loggedin_user.postleitzahl = postleitzahl
            loggedin_user.ort = ort
            loggedin_user.telefonnummer = telefonnummer
            loggedin_user.email = email
            loggedin_user.geburtsdatum = geburtsdatum
            loggedin_user.save()

            return redirect('settings')

        return render(request, 'virtualgovservices/profile_settings.html', {'loggedin_user': loggedin_user})

    if Beamter.objects.filter(user=request.user).exists():
        loggedin_user = Beamter.objects.get(user=request.user)

        if request.method == 'POST':

            if request.FILES.get('profileimg') == None:
                profileimg = loggedin_user.profileimg
                loggedin_user.profileimg = profileimg

            if request.FILES.get('profileimg') != None:
                profileimg = request.FILES.get('profileimg')
                loggedin_user.profileimg = profileimg
                
            anrede = request.POST['anrede']
            vorname = request.POST['vorname']
            nachname = request.POST['nachname']
            telefonnummer = request.POST['telefonnummer']
            raum = request.POST['raum']
            email = request.POST['email']
            

            loggedin_user.anrede = anrede
            loggedin_user.vorname = vorname
            loggedin_user.nachname = nachname
            loggedin_user.telefonnummer = telefonnummer
            loggedin_user.email = email
            loggedin_user.raum = raum
            loggedin_user.save()

            return redirect('settings')
            
        return render(request, 'virtualgovservices/profile_settings_beamte.html', {'loggedin_user': loggedin_user})
        

# Anträge

def übersicht_anträge(request):
    loggedin_user = Buerger.objects.get(user=request.user)

    context = {
            'loggedin_user': loggedin_user,
        }    

    return render(request, 'virtualgovservices/uebersicht_antraege.html', context)

@login_required(login_url='login')
def antrag_annehmen(request, verfahren_id):
    verfahren = get_object_or_404(Verfahren, nummer=verfahren_id)
    verfahren.zustand = 'Antrag angenommen'
    verfahren.save()
    messages.success(request, 'Antrag wurde angenommen.')
    return redirect('meine_antraege')

@login_required(login_url='login')
def verfahren_delegieren(request, verfahren_id):
    if request.method == 'POST':
        neuer_verantwortlicher_id = request.POST.get('neuer_verantwortlicher')
        verfahren = get_object_or_404(Verfahren, nummer=verfahren_id)
        neuer_verantwortlicher = get_object_or_404(Beamter, id=neuer_verantwortlicher_id)
        verfahren.verantwortlicher = neuer_verantwortlicher
        verfahren.save()
        messages.success(request, 'Antrag wurde erfolgreich delegiert.')
        return redirect('meine_antraege')

@login_required(login_url='login')
def bescheid_erstellen(request, verfahren_id):
    verfahren = get_object_or_404(Verfahren, pk=verfahren_id)
    if request.method == 'POST':
        form = BescheidForm(request.POST)
        if form.is_valid():
            dokument = Dokument.objects.create(
                verfahren=verfahren,
                titel=form.cleaned_data['titel'],
                inhalt=form.cleaned_data['inhalt'],
                bemerkungen=form.cleaned_data['bemerkungen'],
                # Sie können hier auch die anderen Felder ausfüllen
            )
            # Generiere die URI und URL des Dokuments
            dokument.save()  # Dies ruft die save-Methode auf, die die URI und URL setzt
            
            verfahren.zustand = 'abgeschlossen'
            verfahren.save()

            messages.success(request, "Der Bescheid wurde erfolgreich erstellt.")
            return redirect('meine_antraege')
        else:
            messages.error(request, "Es gab einen Fehler beim Erstellen des Bescheides.")
            return redirect('meine_antraege')

# @login_required(login_url='login')
def hundeanmeldung(request):
    if request.user.is_authenticated:
        loggedin_user = Buerger.objects.get(user=request.user)
        buerger_form = BuergerDatenForm()
        hundeanmeldung_form = HundeanmeldungForm()  

        if request.method == 'POST':
            buerger_form = BuergerDatenForm(request.POST, instance=loggedin_user)
            hundeanmeldung_form = HundeanmeldungForm(request.POST)
            if buerger_form.is_valid() and hundeanmeldung_form.is_valid():
                buerger_form.save()
                # Erstellen einer neuen Hundeanmeldung
                hundeanmeldung = hundeanmeldung_form.save(commit=False)
                hundeanmeldung.buerger = loggedin_user
                hundeanmeldung.save()

                messages.success(request, "Ihre Anmeldung wurde erfolgreich entgegengenommen!")
                return redirect('/virtualgovservices/')
        
        context = {
            'loggedin_user': loggedin_user,
            'buerger_form': buerger_form,
            'hundeanmeldung_form': hundeanmeldung_form
        }
        return render(request, "virtualgovservices/hundeanmeldung.html", context)
    else:
        messages.error(request, "Um diesen Service nutzen zu können, müssen Sie angemeldet sein!")
        return redirect('login')

# @login_required(login_url='login')
def wohnsitzanmeldung(request):
    if request.user.is_authenticated:
        loggedin_user = Buerger.objects.get(user=request.user)
        buerger_form = BuergerDatenForm()
        wohnsitzanmeldung_form = WohnsitzanmeldungForm()

        if request.method == 'POST':
            buerger_form = BuergerDatenForm(request.POST, instance=loggedin_user)
            wohnsitzanmeldung_form = WohnsitzanmeldungForm(request.POST)
            if buerger_form.is_valid() and wohnsitzanmeldung_form.is_valid():
                buerger_form.save()
                wohnsitzanmeldung = wohnsitzanmeldung_form.save(commit=False)
                wohnsitzanmeldung.buerger = loggedin_user
                wohnsitzanmeldung.save()
                
                messages.success(request, "Ihre Anmeldung wurde erfolgreich entgegengenommen!")
                return redirect('/virtualgovservices/')
        
        context = {
            'loggedin_user': loggedin_user,
            'buerger_form': buerger_form,
            'wohnsitzanmeldung_form': wohnsitzanmeldung_form
        }
        return render(request, "virtualgovservices/wohnsitzanmeldung.html", context)
    else:
        messages.error(request, "Um diesen Service nutzen zu können, müssen Sie angemeldet sein!")
        return redirect('login')


@login_required(login_url='login')
def meine_antraege(request):
    user = request.user
    buerger = Buerger.objects.filter(user=user).first()
    beamter = Beamter.objects.filter(user=user).first()

    if buerger:
        verfahren_liste = Verfahren.objects.filter(antragssteller=user)

        context = {
            'loggedin_user': buerger,
            'verfahren_liste': verfahren_liste,
        }
        return render(request, "virtualgovservices/meine_antraege.html", context)

    elif beamter:
        verfahren_liste = Verfahren.objects.filter(verantwortlicher=beamter)
        beamten_liste = Beamter.objects.exclude(user=user)
        bescheid_form = BescheidForm()

        for verfahren in verfahren_liste:
            buerger = get_object_or_404(Buerger, user=verfahren.antragssteller)
            verfahren.buerger_anrede = buerger.anrede
            verfahren.buerger_vorname = buerger.vorname
            verfahren.buerger_nachname = buerger.nachname
            verfahren.buerger_telefonnummer = buerger.telefonnummer
            verfahren.buerger_email = buerger.email

        context = {
            'loggedin_user': beamter,
            'verfahren_liste': verfahren_liste,
            'beamten_liste': beamten_liste,
            'bescheid_form': bescheid_form,
        }

        return render(request, 'virtualgovservices/beamte_antragsuebersicht.html', context)

def create_signed_xml(antrag, antrag_data):
    # Erstellen des XML-Dokuments aus den Antragsdaten
    root = etree.Element("AntragsDaten")
    for key, value in antrag_data.items():
        tag_name = key.replace(" ", "_")
        element = etree.SubElement(root, tag_name)
        element.text = str(value)

    # Schlüssel und Zertifikat laden
    with open("/home/ubuntu/website/private-key.pem", "rb") as f:
        key = f.read()
    with open("/home/ubuntu/website/certificate.pem", "rb") as f:
        cert = f.read()

    # Signieren des XML-Dokuments
    signer = XMLSigner(method=signxml.methods.enveloped, signature_algorithm="rsa-sha256")
    signed_xml = signer.sign(root, key=key, cert=cert)

    return etree.tostring(signed_xml)

# @login_required(login_url='login')
def dokument_detail_view(request, uuid):
    dokument = get_object_or_404(Dokument, uri=uuid)
    verfahren = dokument.verfahren

    antrag = None
    header2 = None
    antrag_data = {}

    if Hundeanmeldung.objects.filter(dokument=dokument).exists():
        antrag = Hundeanmeldung.objects.get(dokument=dokument)
        header2 = "Angaben zum anzumeldenden Hund"
        antrag_data = {
            'Name': antrag.name_hund,
            'Geschlecht': antrag.geschlecht_hund,
            'Rasse': antrag.rasse_hund,
            'Kampfhund': antrag.kampfhund,
            'Wurftag': antrag.wurftag_hund,
            'Beginn Haltung': antrag.beginn_haltung_hund,
        }

    if Wohnsitzanmeldung.objects.filter(dokument=dokument).exists():
        antrag = Wohnsitzanmeldung.objects.get(dokument=dokument)
        header2 = "Angaben zur neuen Wohnung"
        antrag_data = {
            'Einzugsdatum': antrag.umzugsdatum,
            'Strasse': antrag.neue_strasse,
            'Postleitzahl': antrag.neue_postleitzahl,
            'Ort': antrag.neuer_ort,
        }
    
    signed_xml_str = create_signed_xml(antrag, antrag_data) if antrag else None

    context = {
        'dokument': dokument,
        'verfahren': verfahren,
        'antrag': antrag,
        'header2': header2,
        'antrag_data': antrag_data,
        'signed_xml_str': signed_xml_str,
    }

    # if request.user.is_authenticated:
    #     loggedin_user = Buerger.objects.get(user=request.user)
    #     context['loggedin_user'] = loggedin_user

    return render(request, 'virtualgovservices/base_antrag.html', context)

@login_required(login_url='landing_page')
def statistik(request):
    user = request.user
    buerger = Buerger.objects.filter(user=user).first()
    beamter = Beamter.objects.filter(user=user).first()

    if buerger:
        pass

    elif beamter:
        heute = timezone.now()
        start_datum = heute - timedelta(days=14)

        # Abfragen für Hundeanmeldungen und Wohnsitzanmeldungen
        hundeanmeldungen = (
            Hundeanmeldung.objects.filter(angemeldet_am__range=[start_datum, heute])
            .annotate(tag=TruncDay('angemeldet_am'))
            .values('tag')
            .annotate(anmeldungen=Count('id'))
            .order_by('tag')
        )

        wohnsitzanmeldungen = (
            Wohnsitzanmeldung.objects.filter(angemeldet_am__range=[start_datum, heute])
            .annotate(tag=TruncDay('angemeldet_am'))
            .values('tag')
            .annotate(anmeldungen=Count('id'))
            .order_by('tag')
        )

        # Daten für das Diagramm vorbereiten
        labels = [(start_datum + timedelta(days=i)).strftime('%d.%m.%y') for i in range(15)]
        hund_daten = [0] * 15
        wohn_daten = [0] * 15

        for anmeldung in hundeanmeldungen:
            index = (anmeldung['tag'].date() - start_datum.date()).days
            hund_daten[index] = anmeldung['anmeldungen']

        for anmeldung in wohnsitzanmeldungen:
            index = (anmeldung['tag'].date() - start_datum.date()).days
            wohn_daten[index] = anmeldung['anmeldungen']

        daten = {
            'labels': labels,
            'hundeanmeldungen': hund_daten,
            'wohnsitzanmeldungen': wohn_daten
        }


        context = {
            'loggedin_user': beamter,
            'daten': daten,
        }

        return render(request, 'virtualgovservices/beamte_statistik.html', context)


# APIs

def verfahrensdauer_abfrage(request):
    beamte_ids = request.GET.getlist('beamte')  # IDs der Beamten als URL-Parameter
    themengebiet = request.GET.get('themengebiet')

    verfahrens_query = Verfahren.objects.all()

    if beamte_ids:
        verfahrens_query = verfahrens_query.filter(verantwortlicher_id__in=beamte_ids)
    if themengebiet:
        verfahrens_query = verfahrens_query.filter(themengebiet=themengebiet)

    verfahrens_data = [
        {
            'verfahren_nummer': verfahren.nummer,
            'dauer in tage': (timezone.now() - verfahren.erstellt_am).days  # Berechnet die Dauer in Tagen
        }
        for verfahren in verfahrens_query
    ]

    return JsonResponse(verfahrens_data, safe=False)


@csrf_exempt
def antragstellung(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)

            # Daten, welche abgefragt werden
            buerger_id = data['buerger_id']
            geschlecht_hund = data['geschlecht_hund']
            name_hund = data['name_hund']
            wurftag_hund = data['wurftag_hund']
            rasse_hund = data['rasse_hund']
            kampfhund = data['kampfhund']
            beginn_haltung_hund = data['beginn_haltung_hund']

            # Buerger-Objekt abrufen
            buerger = Buerger.objects.get(id=buerger_id)

            # Verfahren erstellen
            beamter = Beamter.objects.get(zuständigkeit="Hundesteuer")
            verfahren = Verfahren.objects.create(
                antragssteller=buerger.user,
                verantwortlicher=beamter,
                themengebiet="Hundesteuer: Hundeanmeldung",
                aktualisiert_am=timezone.now()
            )

            # Hundeanmeldung erstellen
            hundeanmeldung = Hundeanmeldung.objects.create(
                buerger=buerger,
                verfahren=verfahren,
                geschlecht_hund=geschlecht_hund,
                name_hund=name_hund,
                wurftag_hund=wurftag_hund,
                rasse_hund=rasse_hund,
                kampfhund=kampfhund,
                beginn_haltung_hund=beginn_haltung_hund
            )

            # Dokument erstellen
            dokument = Dokument.objects.create(
                verfahren=verfahren,
                inhalt=f"Hundeanmeldung von {buerger.vorname} {buerger.nachname}"
            )
            hundeanmeldung.dokument = dokument
            hundeanmeldung.save()

            return JsonResponse({"message": "Antrag erfolgreich erstellt"}, status=201)
        except (KeyError, TypeError, ValueError):
            return JsonResponse({"error": "Ungültige Daten"}, status=400)

    return JsonResponse({"error": "Nur POST-Anfragen erlaubt"}, status=405)


def akt_historie_abfrage(request, verfahren_id):
    try:
        verfahren = Verfahren.objects.get(nummer=verfahren_id)
        # Annahme: Verfahren hat Attribute wie 'status', 'historie', etc.
        verfahrens_data = {
            'id': verfahren.nummer,
            'status': verfahren.zustand,
            # 'historie': verfahren.historie
        }
    except Verfahren.DoesNotExist:
        verfahrens_data = {'error': 'Verfahren nicht gefunden'}

    return JsonResponse(verfahrens_data)
