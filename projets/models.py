from django.db import models
from django.urls import reverse


class Projet(models.Model):
    CATEGORIE_CHOICES = [
        ('ascenseur', 'Ascenseur'),
        ('climatisation', 'Climatisation'),
        ('electricite', 'Électricité'),
        ('groupe_electrogene', 'Groupe Électrogène'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    image_principale = models.ImageField(upload_to='projets/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=200)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
    
    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        return reverse('projets:projet_detail', kwargs={'slug': self.slug})
    
    def get_categorie_display_class(self):
        """Retourne la classe CSS selon la catégorie"""
        classes = {
            'ascenseur': 'ascenceur',
            'climatisation': 'climatisation',
            'electricite': 'electricite',
            'groupe_electrogene': 'groupe_electrogene',
        }
        return classes.get(self.categorie, '')


class ImageProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projets/galeries/')
    titre = models.CharField(max_length=200, blank=True)
    ordre = models.IntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordre', 'date_ajout']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
    
    def __str__(self):
        return f"{self.projet.titre} - {self.titre or 'Image'}"

