from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from .functions import generate_qr_code
from django.core.files.base import ContentFile
from django.utils import timezone


class Beamter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    anrede = models.CharField(max_length=10, null=True)
    vorname = models.CharField(max_length=100, null=True)
    nachname = models.CharField(max_length=100, null=True)
    telefonnummer = models.CharField(max_length=20, null=True)
    email = models.EmailField(blank=True, null=True)
    zuständigkeit = models.CharField(max_length=100, null=True)
    nr_zuständigkeit = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.anrede} {self.vorname} {self.nachname}"


class Verfahren(models.Model):
    # Die fortlaufende Nummer wird automatisch als Primärschlüssel zugewiesen
    nummer = models.AutoField(primary_key=True)
    antragssteller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)
    zustand = models.CharField(max_length=100, default="Antrag gestellt")
    # Ein ForeignKey, der das Verfahren einem Beamten zuordnet
    verantwortlicher = models.ForeignKey(Beamter, on_delete=models.CASCADE, null=True)
    # verantwortlicher = models.TextField(default="Beamter X")
    themengebiet = models.CharField(max_length=100)

    def __str__(self):
        return f"Verfahren {self.nummer} - {self.themengebiet}"


class Buerger(models.Model):
    # OneToOneField erstellt eine Eins-zu-Eins-Beziehung mit dem User-Modell
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to = 'virtualgovservices/profile_images/', default = '/virtualgovservices/profile_images/avatar.jpg')
    anrede = models.CharField(max_length=10)
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    strasse = models.CharField(max_length=100)
    postleitzahl = models.CharField(max_length=10) 
    ort = models.CharField(max_length=100)
    telefonnummer = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    geburtsdatum = models.DateField(blank=True, default="1980-01-01")
    
    def __str__(self):
        return f"{self.anrede} {self.vorname} {self.nachname}"


class Dokument(models.Model):
    # Die URI ist eindeutig für jedes Dokument
    uri = models.TextField(unique=True)
    url = models.URLField(blank=True)
    # Jedes Dokument ist einem Verfahren zugeordnet
    verfahren = models.ForeignKey(Verfahren, on_delete=models.CASCADE)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    digitale_signatur = models.TextField(blank=True)  # Placeholder Signatur
    inhalt = models.TextField()
    # Der QR-Code wird beim Speichern des Dokuments generiert und gespeichert
    # qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    # hundeanmeldung = models.ForeignKey(Hundeanmeldung, on_delete=models.CASCADE, null=True, blank=True)

    # Wenn das Dokument neu ist und noch keine URI hat, generieren wir eine
    def save(self, *args, **kwargs):
        if not self.uri:
            self.uri = uuid.uuid4()
            self.url = ("https://193.196.52.181/virtualgovservices/dokumente/" + str(self.uri) + "/")

        # if not self.qr_code:
        #     qr_code_buffer = generate_qr_code(self.url)
        #     self.qr_code.save(f"qr_code_{self.uri}.png", ContentFile(qr_code_buffer.getvalue()), save=False)
            
        super(Dokument, self).save(*args, **kwargs)

    def __str__(self):
        return f"Dokument für Verfahren {self.verfahren.nummer}"


class Hundeanmeldung(models.Model):
    # Ein ForeignKey, der den Antrag dem Bürger zuordnet
    buerger = models.ForeignKey(Buerger, related_name='hundeanmeldungen', on_delete=models.CASCADE)
    angemeldet_am = models.DateTimeField(auto_now_add=True)
    verfahren = models.OneToOneField(Verfahren, on_delete=models.CASCADE, null=True, blank=True)
    geschlecht_hund = models.CharField(max_length=100, null=True)
    name_hund = models.CharField(max_length=100, null=True)
    wurftag_hund = models.DateField(blank=True, null=True)
    rasse_hund = models.CharField(max_length=100, null=True)
    kampfhund = models.CharField(max_length=100, null=True)
    beginn_haltung_hund = models.DateField(blank=True, null=True)
    dokument = models.OneToOneField(Dokument, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.verfahren is None or not self.verfahren.id:
            # Wenn noch kein Verfahren zugeordnet ist, erstellen wir eines
            beamter = Beamter.objects.get(zuständigkeit="Hundesteuer")
            verfahren = Verfahren(
                antragssteller=self.buerger.user,
                verantwortlicher=beamter,
                themengebiet="Hundesteuer: Hundeanmeldung",
                aktualisiert_am=timezone.now()
            )
            verfahren.save()

            # Anschließend verknüpfen wir das Verfahren mit der Anmeldung
            self.verfahren = verfahren

            # und erstellen das dazugehörige Dokument
            dokument = Dokument.objects.create(
                verfahren=self.verfahren,
                inhalt=f"Hundeanmeldung von {self.buerger.vorname} {self.buerger.nachname}",
            )

            if not self.dokument:
                self.dokument = dokument

        # Schließlich speichern wir die Anmeldung
        super(Hundeanmeldung, self).save(*args, **kwargs)

    def __str__(self):
        return f"Anmeldung von {self.buerger.vorname} {self.buerger.nachname} am {self.angemeldet_am.strftime('%d.%m.%Y')}"
      
        

