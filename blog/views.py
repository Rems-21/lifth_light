from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, CategorieArticle


def liste_articles(request, categorie=None):
    """Affiche la liste de tous les articles publiés"""
    articles = Article.objects.filter(publie=True)
    
    # Filtrer par catégorie si demandé
    categorie_obj = None
    if categorie:
        categorie_obj = get_object_or_404(CategorieArticle, slug=categorie)
        articles = articles.filter(categories=categorie_obj)
    
    # Pagination
    paginator = Paginator(articles, 6)  # 6 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupérer toutes les catégories
    categories = CategorieArticle.objects.all()
    
    # Articles récents (pour la sidebar)
    articles_recents = Article.objects.filter(publie=True)[:5]
    
    context = {
        'articles': page_obj,
        'categories': categories,
        'categorie_active': categorie_obj,
        'articles_recents': articles_recents,
    }
    return render(request, 'blog/liste_articles.html', context)


def article_detail(request, slug):
    """Affiche le détail d'un article"""
    article = get_object_or_404(Article, slug=slug, publie=True)
    
    # Incrémenter le compteur de vues
    article.increment_vue()
    
    # Articles récents (pour la sidebar)
    articles_recents = Article.objects.filter(publie=True).exclude(id=article.id)[:5]
    
    # Articles similaires (même catégorie)
    articles_similaires = Article.objects.filter(
        publie=True,
        categories__in=article.categories.all()
    ).exclude(id=article.id).distinct()[:3]
    
    # Navigation précédent/suivant
    article_precedent = Article.objects.filter(
        publie=True,
        date_publication__lt=article.date_publication
    ).order_by('-date_publication').first()
    
    article_suivant = Article.objects.filter(
        publie=True,
        date_publication__gt=article.date_publication
    ).order_by('date_publication').first()
    
    context = {
        'article': article,
        'articles_recents': articles_recents,
        'articles_similaires': articles_similaires,
        'article_precedent': article_precedent,
        'article_suivant': article_suivant,
    }
    return render(request, 'blog/article_detail.html', context)
