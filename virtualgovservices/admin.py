from django.contrib import admin
from .models import Buerger, Hundeanmeldung, Dokument, Verfahren, Beamter, Wohnsitzanmeldung

class BuergerAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'anrede', 'vorname', 'nachname', 'telefonnummer', 'email')
    search_fields = ('vorname', 'nachname', 'telefonnummer', 'email')
    list_filter = ('anrede', 'ort')

# Register your models here.
admin.site.register(Buerger, BuergerAdmin)
admin.site.register(Hundeanmeldung)
admin.site.register(Dokument)
admin.site.register(Verfahren)
admin.site.register(Beamter)
admin.site.register(Wohnsitzanmeldung)


