from django import forms
from .models import Buerger, Hundeanmeldung, Wohnsitzanmeldung, Beamter
from django.forms.widgets import DateInput

class BuergerDatenForm(forms.ModelForm):
    class Meta:
        model = Buerger
        fields = ['anrede', 'vorname', 'nachname', 'strasse', 'postleitzahl', 'ort', 'telefonnummer', 'email', 'geburtsdatum']
        labels = {
            'anrede': 'Anrede',
            'vorname': 'Vorname',
            'nachname': 'Nachname',
            'strasse': 'Strasse',
            'postleitzahl': 'Postleitzahl',
            'ort': 'Wohnort',
            'telefonnummer': 'Telefonnummer',
            'email': 'Email',
            'geburtsdatum': 'Geburtsdatum'
        }
        widgets = {
            'geburtsdatum': forms.DateInput(attrs={'type': 'date'}),
        }

class HundeanmeldungForm(forms.ModelForm):
    class Meta:
        model = Hundeanmeldung
        fields = ['name_hund', 'rasse_hund', 'geschlecht_hund', 'kampfhund', 'wurftag_hund', 'beginn_haltung_hund']
        labels = {
            'name_hund': 'Name',
            'rasse_hund': 'Rasse',
            'geschlecht_hund': 'Geschlecht',
            'kampfhund': 'Kampfhund?',
            'Wurftag_hund': 'Wurftag',
            'beginn_haltung_hund': 'Der Hund wird von mir gehalten seit dem'
        }
        widgets = {
            'geschlecht_hund': forms.RadioSelect(choices=[('männlich', 'Männlich'), ('weiblich', 'Weiblich')]),
            'kampfhund': forms.RadioSelect(choices=[('Ja', 'Ja'), ('Nein', 'Nein')]),
            'wurftag_hund': forms.DateInput(attrs={'type': 'date'}),
            'beginn_haltung_hund': forms.DateInput(attrs={'type': 'date'}),
        }

class WohnsitzanmeldungForm(forms.ModelForm):
    class Meta:
        model = Wohnsitzanmeldung
        fields = ['umzugsdatum', 'neue_strasse', 'neue_postleitzahl', 'neuer_ort', 'vorherige_adresse']
        labels = {
            'umzugsdatum': 'Einzugsdatum',
            'neue_strasse': 'Strasse',
            'neue_postleitzahl': 'Postleitzahl',
            'neuer_ort': 'Ort',
            'vorherige_adresse': 'Bisherige Anschrift',
        }
        widgets = {
            'umzugsdatum': forms.DateInput(attrs={'type': 'date'}),
        }

# class DelegierenForm(forms.Form):
#     neuer_verantwortlicher = forms.ModelChoiceField(
#         queryset=Beamter.objects.all(),
#         label="Neuen Verantwortlichen auswählen",
#         help_text="Wählen Sie einen Beamten aus, an den dieser Antrag delegiert werden soll."
#     )

class BescheidForm(forms.Form):
    titel = forms.CharField(label='Titel', max_length=200)
    inhalt = forms.CharField(label='Inhalt', widget=forms.Textarea)
    bemerkungen = forms.CharField(label='Bemerkungen', widget=forms.Textarea, required=False)