from django.urls import path
from . import views

urlpatterns = [
    path('landingpage', views.landingpage, name='landingpage'),
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('meine_antraege/', views.meine_antraege, name='meine_antraege'),
    path('settings/', views.profile_settings, name='settings'),
    path('hundeanmeldung/', views.hundeanmeldung, name='hundeanmeldung'),
    path('dokumente/<uuid:uuid>/', views.dokument_detail_view, name='dokument_detail'),
]