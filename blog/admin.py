from django.contrib import admin
from .models import Article, CategorieArticle


@admin.register(CategorieArticle)
class CategorieArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'description')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'publie', 'vue')
    list_filter = ('publie', 'date_publication', 'categories')
    search_fields = ('titre', 'contenu', 'auteur')
    prepopulated_fields = {'slug': ('titre',)}
    filter_horizontal = ('categories',)
    readonly_fields = ('date_publication', 'date_modification', 'vue')
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'slug', 'auteur', 'resume')
        }),
        ('Contenu', {
            'fields': ('contenu', 'image_principale')
        }),
        ('Métadonnées', {
            'fields': ('categories', 'publie', 'date_publication', 'date_modification', 'vue')
        }),
    )
