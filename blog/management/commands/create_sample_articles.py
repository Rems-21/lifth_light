from django.core.management.base import BaseCommand
from blog.models import Article, CategorieArticle
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Crée des articles de blog d\'exemple'

    def handle(self, *args, **options):
        # Créer des catégories
        categorie_ascenseur, _ = CategorieArticle.objects.get_or_create(
            nom='Ascenseurs',
            defaults={'description': 'Actualités et conseils sur les ascenseurs'}
        )
        
        categorie_electricite, _ = CategorieArticle.objects.get_or_create(
            nom='Électricité',
            defaults={'description': 'Actualités et conseils sur l\'électricité'}
        )
        
        categorie_climatisation, _ = CategorieArticle.objects.get_or_create(
            nom='Climatisation',
            defaults={'description': 'Actualités et conseils sur la climatisation'}
        )
        
        categorie_actualites, _ = CategorieArticle.objects.get_or_create(
            nom='Actualités',
            defaults={'description': 'Actualités de l\'entreprise'}
        )

        # Articles d'exemple
        articles_data = [
            {
                'titre': 'Nouvelle Installation d\'Ascenseur à Yaoundé',
                'resume': 'Lift and Light a récemment complété l\'installation d\'un ascenseur moderne dans un immeuble résidentiel de Yaoundé. Découvrez les détails de ce projet.',
                'contenu': '''<h2>Un Projet d'Envergure</h2>
                <p>Lift and Light est fier d'annoncer la finalisation d'une nouvelle installation d'ascenseur dans un immeuble résidentiel moderne situé au cœur de Yaoundé. Ce projet représente notre engagement continu envers l'excellence et l'innovation.</p>
                
                <h3>Caractéristiques Techniques</h3>
                <p>L'ascenseur installé est équipé des dernières technologies en matière de sécurité et d'efficacité énergétique. Il dispose de :</p>
                <ul>
                    <li>Système de sécurité avancé conforme aux normes internationales</li>
                    <li>Économie d'énergie optimisée</li>
                    <li>Interface utilisateur intuitive</li>
                    <li>Maintenance facilitée</li>
                </ul>
                
                <h3>Notre Engagement</h3>
                <p>Ce projet témoigne de notre expertise et de notre capacité à livrer des solutions de qualité supérieure dans les délais convenus. Notre équipe de techniciens certifiés a travaillé en étroite collaboration avec les propriétaires pour garantir une installation parfaite.</p>
                
                <p>Pour plus d'informations sur nos services d'installation d'ascenseurs, n'hésitez pas à nous contacter.</p>''',
                'categories': [categorie_ascenseur, categorie_actualites],
                'date_offset': 5
            },
            {
                'titre': 'Conseils pour l\'Entretien de Votre Système Électrique',
                'resume': 'Découvrez nos conseils pratiques pour maintenir votre installation électrique en bon état et éviter les pannes coûteuses.',
                'contenu': '''<h2>L'Importance de la Maintenance</h2>
                <p>Une installation électrique bien entretenue est essentielle pour la sécurité de votre foyer ou de votre entreprise. Voici quelques conseils pratiques pour maintenir votre système électrique en excellent état.</p>
                
                <h3>Vérifications Régulières</h3>
                <ul>
                    <li><strong>Inspection visuelle :</strong> Vérifiez régulièrement l'état de vos prises et interrupteurs</li>
                    <li><strong>Tableau électrique :</strong> Assurez-vous que votre tableau électrique est accessible et bien organisé</li>
                    <li><strong>Fils et câbles :</strong> Inspectez les câbles pour détecter tout signe d'usure ou de dommage</li>
                </ul>
                
                <h3>Signes d'Alerte</h3>
                <p>Si vous remarquez l'un des signes suivants, contactez immédiatement un électricien professionnel :</p>
                <ul>
                    <li>Prises ou interrupteurs chauds au toucher</li>
                    <li>Odeur de brûlé</li>
                    <li>Disjoncteurs qui sautent fréquemment</li>
                    <li>Lumières qui clignotent</li>
                </ul>
                
                <h3>Maintenance Professionnelle</h3>
                <p>Lift and Light propose des contrats de maintenance préventive pour garantir la sécurité et la performance de votre installation électrique. Nos techniciens certifiés effectuent des inspections régulières et peuvent intervenir rapidement en cas d'urgence.</p>''',
                'categories': [categorie_electricite],
                'date_offset': 10
            },
            {
                'titre': 'Optimiser l\'Efficacité de Votre Climatisation',
                'resume': 'Apprenez comment réduire votre consommation d\'énergie tout en maintenant un confort optimal avec votre système de climatisation.',
                'contenu': '''<h2>Économies d'Énergie et Confort</h2>
                <p>Une climatisation bien entretenue et correctement utilisée peut réduire significativement votre consommation d'énergie tout en maintenant un environnement confortable. Voici nos recommandations.</p>
                
                <h3>Bonnes Pratiques</h3>
                <ul>
                    <li><strong>Température optimale :</strong> Réglez votre climatisation à 24-26°C pour un confort optimal</li>
                    <li><strong>Entretien régulier :</strong> Nettoyez les filtres tous les mois pendant la saison chaude</li>
                    <li><strong>Isolation :</strong> Assurez-vous que vos portes et fenêtres sont bien fermées</li>
                    <li><strong>Utilisation intelligente :</strong> Utilisez un thermostat programmable pour optimiser la consommation</li>
                </ul>
                
                <h3>Maintenance Préventive</h3>
                <p>Un entretien régulier par des professionnels permet de :</p>
                <ul>
                    <li>Maintenir l'efficacité énergétique</li>
                    <li>Prolonger la durée de vie de votre équipement</li>
                    <li>Éviter les pannes coûteuses</li>
                    <li>Améliorer la qualité de l'air intérieur</li>
                </ul>
                
                <h3>Nos Services</h3>
                <p>Lift and Light offre des services complets de maintenance et de réparation pour tous types de systèmes de climatisation. Contactez-nous pour un devis personnalisé.</p>''',
                'categories': [categorie_climatisation],
                'date_offset': 15
            },
            {
                'titre': 'Lift and Light : 6 Ans d\'Excellence au Service du Cameroun',
                'resume': 'Retour sur 6 années de croissance et d\'innovation dans le domaine des solutions électriques et d\'ascenseurs au Cameroun.',
                'contenu': '''<h2>Notre Parcours</h2>
                <p>Depuis sa création en 2019, Lift and Light a connu une croissance remarquable, devenant une référence dans le domaine des solutions électriques et d'ascenseurs au Cameroun.</p>
                
                <h3>Nos Réalisations</h3>
                <p>En 6 ans d'activité, nous avons :</p>
                <ul>
                    <li>Réalisé plus de 200 projets d'envergure</li>
                    <li>Servi des centaines de clients satisfaits</li>
                    <li>Établi un réseau de partenaires de confiance</li>
                    <li>Maintenu un taux de satisfaction client exceptionnel</li>
                </ul>
                
                <h3>Notre Vision</h3>
                <p>Notre mission est de continuer à fournir des solutions innovantes et fiables qui améliorent le confort et la qualité de vie de nos clients. Nous investissons continuellement dans la formation de notre équipe et dans les dernières technologies.</p>
                
                <h3>L'Avenir</h3>
                <p>Alors que nous célébrons ces 6 années de succès, nous regardons vers l'avenir avec optimisme. Nous continuerons à innover et à servir nos clients avec le même engagement envers l'excellence qui nous a caractérisés depuis le début.</p>
                
                <p>Merci à tous nos clients et partenaires pour leur confiance continue.</p>''',
                'categories': [categorie_actualites],
                'date_offset': 20
            },
            {
                'titre': 'Groupes Électrogènes : Solutions d\'Alimentation de Secours',
                'resume': 'Découvrez comment un groupe électrogène peut garantir la continuité de vos activités en cas de coupure de courant.',
                'contenu': '''<h2>L'Importance d'une Alimentation de Secours</h2>
                <p>Dans un contexte où les coupures de courant peuvent survenir, un groupe électrogène représente une solution essentielle pour garantir la continuité de vos activités professionnelles ou le confort de votre foyer.</p>
                
                <h3>Types de Groupes Électrogènes</h3>
                <p>Nous proposons différents types de groupes électrogènes adaptés à vos besoins :</p>
                <ul>
                    <li><strong>Résidentiels :</strong> Pour les maisons et petits commerces</li>
                    <li><strong>Industriels :</strong> Pour les grandes installations et usines</li>
                    <li><strong>Portables :</strong> Pour les besoins temporaires ou mobiles</li>
                </ul>
                
                <h3>Avantages</h3>
                <ul>
                    <li>Continuité d'activité en cas de panne</li>
                    <li>Protection des équipements sensibles</li>
                    <li>Confort et sécurité pour les résidences</li>
                    <li>Démarrage automatique disponible</li>
                </ul>
                
                <h3>Installation et Maintenance</h3>
                <p>Lift and Light assure l'installation complète de votre groupe électrogène, incluant :</p>
                <ul>
                    <li>Étude de vos besoins énergétiques</li>
                    <li>Installation professionnelle</li>
                    <li>Mise en service et tests</li>
                    <li>Contrats de maintenance</li>
                </ul>
                
                <p>Contactez-nous pour une évaluation gratuite de vos besoins.</p>''',
                'categories': [categorie_electricite, categorie_actualites],
                'date_offset': 25
            }
        ]

        # Créer les articles
        created_count = 0
        for article_data in articles_data:
            date_publication = timezone.now() - timedelta(days=article_data.pop('date_offset'))
            
            article, created = Article.objects.get_or_create(
                titre=article_data['titre'],
                defaults={
                    'resume': article_data['resume'],
                    'contenu': article_data['contenu'],
                    'auteur': 'Lift and Light',
                    'publie': True,
                    'date_publication': date_publication,
                }
            )
            
            if created:
                # Ajouter les catégories
                article.categories.set(article_data['categories'])
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Article créé : {article.titre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Article déjà existant : {article.titre}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n{created_count} article(s) créé(s) avec succès!')
        )

