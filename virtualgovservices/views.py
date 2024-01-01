from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Buerger, Hundeanmeldung, Dokument, Verfahren
from django.contrib import messages


def landingpage(request):
    return render(request, "virtualgovservices/landingpage.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(main)
        else:
            messages.error(
                request, 'Ungültiger Benutzername oder falsches Passwort!')
            return redirect(login)

    else:
        return render(request, "virtualgovservices/login.html")


def signup(request):
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

            user_model = User.objects.get(username=username)
            new_buerger = Buerger.objects.create(
                user=user_model, id_user=user_model.id)
            new_buerger.save()
            messages.success(request, 'Benutzer erfolgreich angelegt.')
            return redirect("settings")
    else:
        return render(request, "virtualgovservices/signup.html")


@login_required(login_url='landingpage')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Erfolgreich abgemeldet!')
    return redirect('landingpage')


@login_required(login_url='landingpage')
def main(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Buerger.objects.get(user=user_object)
    loggedin_user = Buerger.objects.get(user=request.user)

    context = {
        'user_profile': user_profile,
        'loggedin_user': loggedin_user
    }
    return render(request, 'virtualgovservices/mainpage.html', context)


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


@login_required(login_url='landing_page')
def profile_settings(request):
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


@login_required(login_url='login')
def hundeanmeldung(request):
    loggedin_user = Buerger.objects.get(user=request.user)

    if request.method == 'POST':
        # Daten aus dem Formular
        anrede = request.POST.get('anrede')
        vorname = request.POST.get('vorname')
        nachname = request.POST.get('nachname')
        strasse = request.POST.get('strasse')
        postleitzahl = request.POST.get('postleitzahl')
        ort = request.POST.get('ort')
        telefonnummer = request.POST.get('telefonnummer')
        email = request.POST.get('email')
        geburtsdatum = request.POST.get('geburtsdatum')
        geschlecht_hund = request.POST.get('geschlecht_hund')
        name_hund = request.POST.get('name_hund')
        wurftag_hund = request.POST.get('wurftag_hund')
        rasse_hund = request.POST.get('rasse_hund')
        kampfhund = request.POST.get('kampfhund')
        beginn_haltung_hund = request.POST.get('beginn_haltung_hund')

        # Aktualisieren des Buerger-Objekts
        Buerger.objects.filter(id=loggedin_user.id).update(
            anrede=anrede,
            vorname=vorname,
            nachname=nachname,
            strasse=strasse,
            postleitzahl=postleitzahl,
            ort=ort,
            telefonnummer=telefonnummer,
            email=email,
            geburtsdatum=geburtsdatum
        )

        # Erstellen einer neuen Hundeanmeldung
        Hundeanmeldung.objects.create(buerger=loggedin_user, geschlecht_hund=geschlecht_hund, name_hund=name_hund, wurftag_hund=wurftag_hund, rasse_hund=rasse_hund, kampfhund=kampfhund, beginn_haltung_hund=beginn_haltung_hund)

        messages.success(request, "Ihre Anmeldung wurde erfolgreich entgegengenommen!")
        return redirect('/virtualgovservices/')

    context = {
        'loggedin_user': loggedin_user
    }
    return render(request, "virtualgovservices/hundeanmeldung.html", context)


@login_required(login_url='login')
def meine_antraege(request):
    loggedin_user = Buerger.objects.get(user=request.user)
    verfahren_liste = Verfahren.objects.filter(antragssteller=loggedin_user.user)
    hundeanmeldungen = Hundeanmeldung.objects.filter(buerger=loggedin_user)

    context = {
        'loggedin_user': loggedin_user,
        'verfahren_liste': verfahren_liste,
        'hundeanmeldungen': hundeanmeldungen
    }
    return render(request, "virtualgovservices/meine_antraege.html", context)


# @login_required(login_url='login')
def dokument_detail_view(request, uuid):
    if request.user.is_authenticated:
        loggedin_user = Buerger.objects.get(user=request.user)
        hundeanmeldung = Hundeanmeldung.objects.get(buerger=loggedin_user, dokument__uri=uuid)
        dokument = Dokument.objects.get(uri=uuid)
        context = {
            'loggedin_user': loggedin_user,
            'hundeanmeldung': hundeanmeldung,
            'dokument': dokument
        }
        return render(request, 'virtualgovservices/base_antrag.html', context)
    else:
        hundeanmeldung = Hundeanmeldung.objects.get(dokument__uri=uuid)
        dokument = Dokument.objects.get(uri=uuid)
        context = {
            'hundeanmeldung': hundeanmeldung,
            'dokument': dokument
        }
        return render(request, 'virtualgovservices/base_antrag.html', context) 
    

