from django.urls import path
from . import views

urlpatterns = [
    path('landingpage', views.landingpage, name='landingpage'),
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('anträge/', views.übersicht_anträge, name='übersicht_anträge'),
    path('antrag_annehmen/<int:verfahren_id>/', views.antrag_annehmen, name='antrag_annehmen'),
    path('verfahren_delegieren/<int:verfahren_id>/', views.verfahren_delegieren, name='verfahren_delegieren'),
    path('bescheid_erstellen/<int:verfahren_id>/', views.bescheid_erstellen, name='bescheid_erstellen'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('meine_antraege/', views.meine_antraege, name='meine_antraege'),
    path('settings/', views.profile_settings, name='settings'),
    # path('settings_beamte/', views.profile_settings_beamte, name='settings_beamte'),
    path('hundeanmeldung/', views.hundeanmeldung, name='hundeanmeldung'),
    path('wohnsitzanmeldung/', views.wohnsitzanmeldung, name='wohnsitzanmeldung'),
    path('dokumente/<uuid:uuid>/', views.dokument_detail_view, name='dokument_detail'),
    path('statistik/', views.statistik, name='statistik'),
    # APIs
    path('api/verfahrensdauer/', views.verfahrensdauer_abfrage),
    path('api/antragstellung/', views.antragstellung),
    path('api/akt_historie/<int:verfahren_id>/', views.akt_historie_abfrage),
]