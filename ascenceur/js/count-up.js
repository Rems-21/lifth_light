/**
 * Animation de décompte pour les chiffres
 * Utilise Intersection Observer pour déclencher l'animation quand l'élément est visible
 */

(function() {
    'use strict';

    /**
     * Extrait le nombre d'une chaîne (ex: "500+" -> 500, "98%" -> 98, "24/7" -> 24)
     */
    function extractNumber(text) {
        // Cas spécial pour "24/7"
        if (text.includes('/')) {
            const parts = text.split('/');
            return parseFloat(parts[0]) || 0;
        }
        // Enlever tous les caractères non numériques sauf le point
        const cleaned = text.replace(/[^\d.]/g, '');
        return parseFloat(cleaned) || 0;
    }

    /**
     * Extrait le suffixe d'une chaîne (ex: "500+" -> "+", "98%" -> "%", "24/7" -> "/7")
     */
    function extractSuffix(text) {
        // Cas spécial pour "24/7"
        if (text.includes('/')) {
            const parts = text.split('/');
            return '/' + (parts[1] || '');
        }
        const match = text.match(/[^\d.]+$/);
        return match ? match[0] : '';
    }

    /**
     * Formate un nombre avec son suffixe
     */
    function formatNumber(num, suffix) {
        // Pour les nombres décimaux, garder 2 décimales max
        if (num % 1 !== 0) {
            return num.toFixed(2) + suffix;
        }
        return Math.floor(num) + suffix;
    }

    /**
     * Anime un nombre de start à end
     */
    function animateValue(element, start, end, duration, suffix) {
        const startTime = performance.now();
        const isDecimal = end % 1 !== 0;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            
            const current = start + (end - start) * easeOut;
            
            if (isDecimal) {
                element.textContent = formatNumber(current, suffix);
            } else {
                element.textContent = Math.floor(current) + suffix;
            }
            
            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                // S'assurer que la valeur finale est exacte
                element.textContent = formatNumber(end, suffix);
            }
        }
        
        requestAnimationFrame(update);
    }

    /**
     * Initialise l'animation pour un élément
     */
    function initCountUp(element) {
        const originalText = element.textContent.trim();
        const targetValue = extractNumber(originalText);
        const suffix = extractSuffix(originalText);
        
        if (targetValue === 0) return;
        
        // Stocker les valeurs originales
        element.dataset.targetValue = targetValue;
        element.dataset.suffix = suffix;
        
        // Commencer à 0
        element.textContent = '0' + suffix;
    }

    /**
     * Déclenche l'animation pour un élément
     */
    function triggerCountUp(element) {
        if (element.dataset.animated === 'true') return;
        
        const targetValue = parseFloat(element.dataset.targetValue);
        const suffix = element.dataset.suffix || '';
        const duration = parseInt(element.dataset.duration) || 2000; // 2 secondes par défaut
        
        element.dataset.animated = 'true';
        animateValue(element, 0, targetValue, duration, suffix);
    }

    /**
     * Initialise tous les compteurs sur la page
     */
    function initCountUps() {
        // Sélectionner tous les éléments avec la classe count-up ou contenant des chiffres avec + ou %
        const countElements = document.querySelectorAll('.count-up, h3.text-primary, h5.text-primary');
        
        countElements.forEach(function(element) {
            const text = element.textContent.trim();
            // Vérifier si l'élément contient un nombre avec +, % ou /
            if (/\d+[+%]/.test(text) || /\d+\/\d+/.test(text)) {
                element.classList.add('count-up');
                initCountUp(element);
            }
        });

        // Utiliser Intersection Observer pour déclencher l'animation quand l'élément est visible
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.3 // Déclencher quand 30% de l'élément est visible
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting && entry.target.classList.contains('count-up')) {
                    triggerCountUp(entry.target);
                    // Ne plus observer cet élément après l'animation
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observer tous les éléments avec la classe count-up
        document.querySelectorAll('.count-up').forEach(function(element) {
            observer.observe(element);
        });
    }

    // Initialiser quand le DOM est prêt
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCountUps);
    } else {
        initCountUps();
    }
})();

