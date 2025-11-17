"""
Django management command to optimize images
Usage: python manage.py optimize_images
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import os

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Command(BaseCommand):
    help = 'Optimize images in the static files directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=85,
            help='JPEG quality (1-100, default: 85)',
        )
        parser.add_argument(
            '--webp',
            action='store_true',
            help='Create WebP versions of images',
        )
        parser.add_argument(
            '--resize',
            action='store_true',
            help='Create responsive versions (small/medium/large)',
        )

    def handle(self, *args, **options):
        if not PIL_AVAILABLE:
            self.stdout.write(
                self.style.ERROR(
                    'Pillow is not installed. Install it with: pip install Pillow'
                )
            )
            return

        quality = options['quality']
        create_webp = options['webp']
        create_resize = options['resize']

        # Chemin vers les images
        images_dir = Path(settings.STATICFILES_DIRS[0]) / 'images'
        
        if not images_dir.exists():
            self.stdout.write(
                self.style.ERROR(f'Images directory not found: {images_dir}')
            )
            return

        # Formats d'images supportés
        image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
        
        optimized_count = 0
        webp_count = 0
        resize_count = 0

        for image_path in images_dir.rglob('*'):
            if image_path.suffix not in image_extensions:
                continue

            try:
                # Ouvrir l'image
                with Image.open(image_path) as img:
                    # Convertir en RGB si nécessaire (pour JPG)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        if image_path.suffix.lower() in ('.jpg', '.jpeg'):
                            # Créer un fond blanc pour les images avec transparence
                            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = rgb_img
                        else:
                            img = img.convert('RGB')

                    # Optimiser l'image originale
                    original_size = image_path.stat().st_size
                    
                    if image_path.suffix.lower() in ('.jpg', '.jpeg'):
                        img.save(
                            image_path,
                            'JPEG',
                            quality=quality,
                            optimize=True,
                            progressive=True
                        )
                    else:
                        img.save(
                            image_path,
                            'PNG',
                            optimize=True
                        )

                    new_size = image_path.stat().st_size
                    saved = original_size - new_size
                    saved_percent = (saved / original_size * 100) if original_size > 0 else 0

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ {image_path.name}: '
                            f'{original_size / 1024:.1f}KB → {new_size / 1024:.1f}KB '
                            f'(-{saved_percent:.1f}%)'
                        )
                    )
                    optimized_count += 1

                    # Créer version WebP
                    if create_webp:
                        webp_path = image_path.with_suffix('.webp')
                        img.save(webp_path, 'WEBP', quality=quality, method=6)
                        webp_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'  → Created {webp_path.name}')
                        )

                    # Créer versions responsive
                    if create_resize:
                        sizes = {
                            'small': 480,
                            'medium': 768,
                            'large': 1200,
                        }

                        for size_name, max_size in sizes.items():
                            if max(img.size) <= max_size:
                                continue

                            # Calculer les nouvelles dimensions
                            ratio = min(max_size / max(img.size), 1.0)
                            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))

                            # Redimensionner
                            resized = img.resize(new_size, Image.Resampling.LANCZOS)

                            # Nom du fichier
                            size_suffix = f'-{size_name}'
                            resized_path = image_path.parent / f'{image_path.stem}{size_suffix}{image_path.suffix}'

                            # Sauvegarder
                            if image_path.suffix.lower() in ('.jpg', '.jpeg'):
                                resized.save(
                                    resized_path,
                                    'JPEG',
                                    quality=quality,
                                    optimize=True
                                )
                            else:
                                resized.save(resized_path, 'PNG', optimize=True)

                            resize_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'  → Created {resized_path.name}')
                            )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error processing {image_path.name}: {str(e)}')
                )

        # Résumé
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Optimized: {optimized_count} images'
            )
        )
        if create_webp:
            self.stdout.write(
                self.style.SUCCESS(f'✓ WebP created: {webp_count} images')
            )
        if create_resize:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Responsive versions: {resize_count} images')
            )

