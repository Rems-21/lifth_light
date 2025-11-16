// Script d'optimisation des médias pour Lift and Light
// Ce script utilise des techniques modernes pour optimiser les images et vidéos

class MediaOptimizer {
    constructor() {
        this.supportedFormats = {
            images: ['webp', 'avif', 'jpeg', 'png'],
            videos: ['mp4', 'webm', 'av1']
        };
    }

    // Optimisation des images avec lazy loading
    optimizeImages() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback pour les navigateurs plus anciens
            images.forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                img.classList.add('loaded');
            });
        }
    }

    // Optimisation des vidéos
    optimizeVideos() {
        const videos = document.querySelectorAll('video');
        
        videos.forEach(video => {
            // Chargement progressif
            video.addEventListener('loadstart', () => {
                video.classList.add('loading');
            });
            
            video.addEventListener('canplay', () => {
                video.classList.remove('loading');
                video.classList.add('ready');
            });
            
            // Optimisation de la mémoire
            video.addEventListener('pause', () => {
                if (video.currentTime > 0) {
                    video.currentTime = 0;
                }
            });
        });
    }

    // Compression d'images côté client (pour les images uploadées)
    compressImage(file, maxWidth = 1920, quality = 0.8) {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            img.onload = () => {
                // Calculer les nouvelles dimensions
                let { width, height } = img;
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                // Dessiner l'image redimensionnée
                ctx.drawImage(img, 0, 0, width, height);
                
                // Convertir en WebP si supporté
                const format = this.supportsWebP() ? 'image/webp' : 'image/jpeg';
                canvas.toBlob(resolve, format, quality);
            };
            
            img.src = URL.createObjectURL(file);
        });
    }

    // Vérifier le support WebP
    supportsWebP() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }

    // Vérifier le support AVIF
    supportsAVIF() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/avif').indexOf('data:image/avif') === 0;
    }

    // Optimisation des polices
    optimizeFonts() {
        // Preload des polices critiques
        const fontPreload = document.createElement('link');
        fontPreload.rel = 'preload';
        fontPreload.href = 'https://fonts.googleapis.com/css2?family=Outfit:wght@100;200;400;700&display=swap';
        fontPreload.as = 'style';
        document.head.appendChild(fontPreload);
    }

    // Initialiser toutes les optimisations
    init() {
        this.optimizeImages();
        this.optimizeVideos();
        this.optimizeFonts();
        
        // Ajouter des classes CSS pour les animations de chargement
        this.addLoadingStyles();
    }

    // Ajouter des styles CSS pour les animations de chargement
    addLoadingStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .lazy {
                opacity: 0;
                transition: opacity 0.3s;
            }
            
            .loaded {
                opacity: 1;
            }
            
            .loading {
                background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
                background-size: 200% 100%;
                animation: loading 1.5s infinite;
            }
            
            @keyframes loading {
                0% { background-position: 200% 0; }
                100% { background-position: -200% 0; }
            }
            
            video.ready {
                opacity: 1;
                transition: opacity 0.5s;
            }
            
            video.loading {
                opacity: 0.7;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialiser l'optimiseur quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    const optimizer = new MediaOptimizer();
    optimizer.init();
});

// Exporter pour utilisation dans d'autres scripts
window.MediaOptimizer = MediaOptimizer;

