from django.urls import path
from . import views

app_name = 'projets'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projets/<slug:slug>/', views.projet_detail, name='projet_detail'),
]

