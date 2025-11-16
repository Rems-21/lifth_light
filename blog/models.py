from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CategorieArticle(models.Model):
    """Catégories pour les articles"""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(unique=True, max_length=100, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        ordering = ['nom']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:liste_articles_categorie', kwargs={'categorie': self.slug})


class Article(models.Model):
    """Modèle pour les articles de blog/actualités"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, max_length=200, blank=True, verbose_name="Slug")
    auteur = models.CharField(max_length=100, default="Lift and Light", verbose_name="Auteur")
    contenu = models.TextField(verbose_name="Contenu")
    resume = models.TextField(max_length=500, help_text="Résumé court de l'article (max 500 caractères)", verbose_name="Résumé")
    image_principale = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Image principale")
    categories = models.ManyToManyField(CategorieArticle, related_name='articles', blank=True, verbose_name="Catégories")
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    publie = models.BooleanField(default=True, verbose_name="Publié")
    vue = models.IntegerField(default=0, verbose_name="Nombre de vues")
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    
    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})
    
    def increment_vue(self):
        """Incrémente le compteur de vues"""
        self.vue += 1
        self.save(update_fields=['vue'])
