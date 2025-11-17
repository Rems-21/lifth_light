# 🚀 Guide d'Optimisation des Images et Vidéos

## 📋 Stratégies d'Optimisation

### 1. **Lazy Loading** ✅ (Déjà partiellement implémenté)

**Principe :** Charger les images/vidéos uniquement quand elles sont visibles à l'écran.

**Implémentation :**
- ✅ Utiliser `loading="lazy"` sur toutes les images non critiques
- ✅ Utiliser `loading="eager"` uniquement pour le logo (au-dessus de la ligne de flottaison)
- ✅ Pour les vidéos : `preload="metadata"` ou `preload="none"`

### 2. **Preload des Ressources Critiques** ✅ (Déjà implémenté)

**Principe :** Précharger uniquement les ressources essentielles pour le rendu initial.

**Ressources critiques à preload :**
- Logo (visible immédiatement)
- Image/vidéo du hero (au-dessus de la ligne de flottaison)
- CSS critiques

**À éviter :**
- ❌ Ne pas preload toutes les images
- ❌ Ne pas preload les vidéos lourdes

### 3. **Responsive Images avec srcset**

**Principe :** Servir différentes tailles d'images selon la taille d'écran.

```html
<img src="image.jpg" 
     srcset="image-small.jpg 480w,
             image-medium.jpg 768w,
             image-large.jpg 1200w"
     sizes="(max-width: 480px) 100vw,
            (max-width: 768px) 50vw,
            33vw"
     alt="Description"
     loading="lazy">
```

### 4. **Formats Modernes (WebP avec Fallback)**

**Principe :** Utiliser WebP (30% plus léger) avec fallback JPG/PNG.

```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

### 5. **Optimisation Vidéo**

**Principe :** Réduire la taille des vidéos sans perte de qualité visible.

**Techniques :**
- Compression H.264/H.265
- Réduction de la résolution (max 1920x1080 pour web)
- Réduction du framerate (24-30 fps suffit)
- Poster image pour éviter le chargement immédiat

### 6. **Compression d'Images**

**Outils recommandés :**
- **TinyPNG** (https://tinypng.com) - Compression PNG/JPG
- **Squoosh** (https://squoosh.app) - Compression avancée
- **ImageOptim** (Mac) / **FileOptimizer** (Windows)
- **Pillow** (Python) pour compression automatique

**Objectifs :**
- JPG : Qualité 80-85% (bon compromis)
- PNG : Compression optimale
- WebP : Qualité 80-90%

### 7. **Intersection Observer pour Lazy Loading Avancé**

**Principe :** Charger les images quand elles sont proches du viewport.

```javascript
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('img.lazy').forEach(img => {
  imageObserver.observe(img);
});
```

---

## 🛠️ Implémentation

### Étape 1 : Ajouter Lazy Loading Partout

**Images critiques (logo, hero) :**
```html
<img src="logo.jpg" loading="eager" alt="Logo">
```

**Images non critiques :**
```html
<img src="image.jpg" loading="lazy" alt="Description">
```

### Étape 2 : Optimiser les Vidéos

**Vidéo hero :**
```html
<video autoplay loop muted playsinline 
       poster="poster.jpg" 
       preload="metadata">
  <source src="video.mp4" type="video/mp4">
</video>
```

**Vidéos non critiques :**
```html
<video controls preload="none" poster="poster.jpg">
  <source src="video.mp4" type="video/mp4">
</video>
```

### Étape 3 : Créer des Versions Optimisées

**Structure recommandée :**
```
images/
  logo.jpg (original)
  logo.webp (optimisé)
  logo-small.jpg (480px)
  logo-medium.jpg (768px)
  logo-large.jpg (1200px)
```

### Étape 4 : Script d'Optimisation Automatique

Créer un script Python pour :
- Convertir JPG/PNG en WebP
- Créer des versions responsive
- Compresser automatiquement

---

## 📊 Résultats Attendus

**Avant optimisation :**
- Taille totale images : ~5-10 MB
- Temps de chargement : 5-10 secondes
- Score PageSpeed : 40-60

**Après optimisation :**
- Taille totale images : ~1-2 MB
- Temps de chargement : 1-2 secondes
- Score PageSpeed : 80-95

---

## 🔧 Outils et Ressources

### Compression
- **TinyPNG** : https://tinypng.com
- **Squoosh** : https://squoosh.app
- **ImageOptim** : https://imageoptim.com

### Analyse
- **PageSpeed Insights** : https://pagespeed.web.dev
- **GTmetrix** : https://gtmetrix.com
- **WebPageTest** : https://www.webpagetest.org

### Conversion
- **FFmpeg** (vidéos) : https://ffmpeg.org
- **cwebp** (WebP) : https://developers.google.com/speed/webp

---

## ✅ Checklist d'Optimisation

- [ ] Toutes les images non critiques ont `loading="lazy"`
- [ ] Images critiques ont `loading="eager"`
- [ ] Vidéos utilisent `preload="metadata"` ou `preload="none"`
- [ ] Toutes les images sont compressées (qualité 80-85%)
- [ ] Formats WebP créés avec fallback
- [ ] Versions responsive créées (small/medium/large)
- [ ] Poster images pour toutes les vidéos
- [ ] Vidéos compressées (résolution max 1920x1080)
- [ ] Preload uniquement pour ressources critiques
- [ ] Alt text sur toutes les images

---

## 🎯 Priorités

1. **Urgent** : Ajouter `loading="lazy"` partout
2. **Important** : Compresser toutes les images existantes
3. **Recommandé** : Créer versions WebP
4. **Optionnel** : Implémenter srcset responsive

---

**Note :** Commencez par les optimisations simples (lazy loading, compression) qui donnent 80% des résultats avec 20% d'effort !

