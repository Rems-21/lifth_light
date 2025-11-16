from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.conf import settings
import os
import re
from .models import Projet, ImageProjet


def serve_static_html(request, path):
    """Sert les fichiers HTML statiques en remplaçant les chemins relatifs par les chemins statiques Django"""
    # Le path depuis l'URL regex est juste le nom du fichier (ex: about.html)
    # On doit le chercher dans le dossier ascenceur
    html_path = os.path.join(settings.STATICFILES_DIRS[0], path)
    
    if not os.path.exists(html_path):
        raise Http404(f"Fichier {path} non trouvé")
    
    # Lire les fichiers partiels
    partials_dir = os.path.join(settings.STATICFILES_DIRS[0], 'partials')
    navbar_path = os.path.join(partials_dir, 'navbar.html')
    footer_path = os.path.join(partials_dir, 'footer.html')
    
    navbar_content = ""
    footer_content = ""
    
    if os.path.exists(navbar_path):
        with open(navbar_path, 'r', encoding='utf-8') as f:
            navbar_content = f.read()
    
    if os.path.exists(footer_path):
        with open(footer_path, 'r', encoding='utf-8') as f:
            footer_content = f.read()
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer ou insérer les sections navbar et footer par les fichiers partiels
    # Pattern pour trouver la navbar (de <nav jusqu'à </nav>)
    nav_pattern = r'<nav[^>]*>.*?</nav>\s*'
    if navbar_content:
        # Si une navbar existe, la remplacer
        if re.search(nav_pattern, content, flags=re.DOTALL):
            content = re.sub(nav_pattern, navbar_content, content, flags=re.DOTALL)
        else:
            # Sinon, insérer la navbar avant <main> ou après <body>
            # Nettoyer l'indentation du fichier partiel (enlever les espaces en début de ligne)
            navbar_clean = '\n'.join(line.lstrip() if line.strip() else line for line in navbar_content.split('\n'))
            if '<main>' in content:
                # Trouver l'indentation de <main>
                main_match = re.search(r'(\s*)<main>', content)
                indent = main_match.group(1) if main_match else '        '
                # Indenter le contenu de la navbar
                navbar_indented = '\n'.join(indent + line if line.strip() else line for line in navbar_clean.split('\n'))
                content = content.replace('<main>', f'{navbar_indented}\n\n{indent}<main>', 1)
            elif '<body>' in content:
                # Trouver l'indentation de <body>
                body_match = re.search(r'(\s*)<body>', content)
                indent = body_match.group(1) if body_match else '    '
                # Insérer après <body> avec la bonne indentation
                navbar_indented = '\n'.join(indent + line if line.strip() else line for line in navbar_clean.split('\n'))
                content = content.replace('<body>', f'<body>\n\n{navbar_indented}', 1)
    
    # Pattern pour trouver le footer (de <footer jusqu'à </footer>)
    footer_pattern = r'<footer[^>]*>.*?</footer>\s*'
    if footer_content:
        # Si un footer existe, le remplacer
        if re.search(footer_pattern, content, flags=re.DOTALL):
            content = re.sub(footer_pattern, footer_content, content, flags=re.DOTALL)
        else:
            # Sinon, insérer le footer après </main> ou avant les scripts JavaScript
            # Nettoyer l'indentation du fichier partiel
            footer_clean = '\n'.join(line.lstrip() if line.strip() else line for line in footer_content.split('\n'))
            if '</main>' in content:
                # Trouver l'indentation de </main>
                main_match = re.search(r'(\s*)</main>', content)
                indent = main_match.group(1) if main_match else '        '
                # Indenter le contenu du footer
                footer_indented = '\n'.join(indent + line if line.strip() else line for line in footer_clean.split('\n'))
                content = content.replace('</main>', f'</main>\n\n{footer_indented}', 1)
            elif '<!-- JAVASCRIPT FILES -->' in content:
                # Trouver l'indentation du commentaire
                js_match = re.search(r'(\s*)<!-- JAVASCRIPT FILES -->', content)
                indent = js_match.group(1) if js_match else '        '
                footer_indented = '\n'.join(indent + line if line.strip() else line for line in footer_clean.split('\n'))
                content = content.replace('<!-- JAVASCRIPT FILES -->', f'{footer_indented}\n\n{indent}<!-- JAVASCRIPT FILES -->', 1)
            elif '<script' in content:
                # Trouver l'indentation du premier script
                script_match = re.search(r'(\s*)<script', content)
                indent = script_match.group(1) if script_match else '        '
                footer_indented = '\n'.join(indent + line if line.strip() else line for line in footer_clean.split('\n'))
                content = re.sub(r'(<script)', rf'{footer_indented}\n\n{indent}\1', content, count=1)
    
    # Ajouter le bouton WhatsApp flottant avant les scripts JavaScript
    whatsapp_button = '''        <!-- WhatsApp Floating Button -->
        <a href="https://wa.me/237696926678?text=Bonjour,%20je%20souhaite%20obtenir%20plus%20d'informations%20sur%20vos%20services" 
           class="whatsapp-float" 
           target="_blank" 
           rel="noopener noreferrer"
           aria-label="Contactez-nous sur WhatsApp">
            <i class="bi-whatsapp"></i>
        </a>

'''
    
    # Insérer le bouton WhatsApp avant les scripts JavaScript (seulement s'il n'existe pas déjà)
    if 'whatsapp-float' not in content:
        if '<!-- JAVASCRIPT FILES -->' in content:
            js_match = re.search(r'(\s*)<!-- JAVASCRIPT FILES -->', content)
            indent = js_match.group(1) if js_match else '        '
            whatsapp_indented = '\n'.join(indent + line if line.strip() else line for line in whatsapp_button.strip().split('\n'))
            content = content.replace('<!-- JAVASCRIPT FILES -->', f'{whatsapp_indented}\n{indent}<!-- JAVASCRIPT FILES -->', 1)
        elif '<script' in content:
            script_match = re.search(r'(\s*)<script', content)
            indent = script_match.group(1) if script_match else '        '
            whatsapp_indented = '\n'.join(indent + line if line.strip() else line for line in whatsapp_button.strip().split('\n'))
            content = re.sub(r'(<script)', rf'{whatsapp_indented}\n{indent}\1', content, count=1)
    
    # Remplacer les chemins relatifs par les chemins statiques Django
    static_url = settings.STATIC_URL.rstrip('/')  # Enlever le slash final si présent
    
    # CSS - avec et sans guillemets
    content = re.sub(r'href=["\']css/', f'href="{static_url}/css/', content)
    
    # Images - avec et sans guillemets
    content = re.sub(r'(src|href)=["\']images/', rf'\1="{static_url}/images/', content)
    
    # JavaScript - avec et sans guillemets
    content = re.sub(r'src=["\']js/', f'src="{static_url}/js/', content)
    
    # Videos - avec et sans guillemets
    content = re.sub(r'src=["\']video/', f'src="{static_url}/video/', content)
    
    # Liens HTML
    projets_url = reverse("projets:liste_projets")
    content = content.replace('href="index.html"', 'href="/"')
    content = content.replace("href='index.html'", "href='/'")
    content = content.replace('href="projets.html"', f'href="{projets_url}"')
    content = content.replace("href='projets.html'", f"href='{projets_url}'")
    content = content.replace('href="about.html"', 'href="/ascenceur/about.html"')
    content = content.replace("href='about.html'", "href='/ascenceur/about.html'")
    content = content.replace('href="contact.html"', 'href="/ascenceur/contact.html"')
    content = content.replace("href='contact.html'", "href='/ascenceur/contact.html'")
    content = content.replace('href="services.html"', 'href="/ascenceur/services.html"')
    content = content.replace("href='services.html'", "href='/ascenceur/services.html'")
    content = content.replace('href="ascenseurs.html"', 'href="/ascenceur/ascenseurs.html"')
    content = content.replace("href='ascenseurs.html'", "href='/ascenceur/ascenseurs.html'")
    content = content.replace('href="climatisation.html"', 'href="/ascenceur/climatisation.html"')
    content = content.replace("href='climatisation.html'", "href='/ascenceur/climatisation.html'")
    content = content.replace('href="electricite.html"', 'href="/ascenceur/electricite.html"')
    content = content.replace("href='electricite.html'", "href='/ascenceur/electricite.html'")
    content = content.replace('href="groupes-electrogenes.html"', 'href="/ascenceur/groupes-electrogenes.html"')
    content = content.replace("href='groupes-electrogenes.html'", "href='/ascenceur/groupes-electrogenes.html'")
    
    return HttpResponse(content)


def accueil(request):
    """Affiche la page d'accueil statique"""
    return serve_static_html(request, 'index.html')


def liste_projets(request):
    """Affiche la liste de tous les projets actifs"""
    projets = Projet.objects.filter(actif=True)
    
    # Filtrer par catégorie si demandé
    categorie = request.GET.get('categorie')
    if categorie:
        projets = projets.filter(categorie=categorie)
    
    context = {
        'projets': projets,
        'categorie_active': categorie,
    }
    return render(request, 'projets/liste_projets.html', context)


def projet_detail(request, slug):
    """Affiche le détail d'un projet avec sa galerie"""
    projet = get_object_or_404(Projet, slug=slug, actif=True)
    images = projet.images.all()
    
    context = {
        'projet': projet,
        'images': images,
    }
    return render(request, 'projets/projet_detail.html', context)
