from django.contrib import admin
from .models import Projet, ImageProjet


class ImageProjetInline(admin.TabularInline):
    model = ImageProjet
    extra = 1
    fields = ('image', 'titre', 'ordre')


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_creation', 'actif')
    list_filter = ('categorie', 'actif', 'date_creation')
    search_fields = ('titre', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    inlines = [ImageProjetInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'slug', 'description', 'categorie', 'image_principale', 'actif')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_creation', 'date_modification')


@admin.register(ImageProjet)
class ImageProjetAdmin(admin.ModelAdmin):
    list_display = ('projet', 'titre', 'ordre', 'date_ajout')
    list_filter = ('projet', 'date_ajout')
    search_fields = ('projet__titre', 'titre')

