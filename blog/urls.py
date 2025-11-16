from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.liste_articles, name='liste_articles'),
    path('categorie/<slug:categorie>/', views.liste_articles, name='liste_articles_categorie'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]

