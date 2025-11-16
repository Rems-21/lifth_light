# Script PowerShell pour optimiser les médias de Lift and Light
# Ce script compresse les images et vidéos pour améliorer les performances

Write-Host "🚀 Optimisation des médias pour Lift and Light" -ForegroundColor Green

# Vérifier si ImageMagick est installé
$magickPath = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magickPath) {
    Write-Host "❌ ImageMagick n'est pas installé. Installation en cours..." -ForegroundColor Red
    Write-Host "Veuillez installer ImageMagick depuis: https://imagemagick.org/script/download.php#windows" -ForegroundColor Yellow
    Write-Host "Ou utilisez: winget install ImageMagick.ImageMagick" -ForegroundColor Yellow
    exit 1
}

# Créer le dossier optimisé s'il n'existe pas
$optimizedDir = "optimized"
if (-not (Test-Path $optimizedDir)) {
    New-Item -ItemType Directory -Path $optimizedDir
    New-Item -ItemType Directory -Path "$optimizedDir\images"
    New-Item -ItemType Directory -Path "$optimizedDir\video"
}

Write-Host "📁 Dossiers créés: $optimizedDir" -ForegroundColor Blue

# Fonction pour optimiser les images
function Optimize-Image {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [int]$Quality = 85,
        [int]$MaxWidth = 1920
    )
    
    try {
        # Convertir en WebP avec compression
        magick $InputPath -resize "${MaxWidth}x>" -quality $Quality -define webp:lossless=false $OutputPath
        Write-Host "✅ Optimisé: $InputPath -> $OutputPath" -ForegroundColor Green
        
        # Créer aussi une version JPEG optimisée comme fallback
        $jpegPath = $OutputPath -replace '\.webp$', '.jpg'
        magick $InputPath -resize "${MaxWidth}x>" -quality $Quality $jpegPath
        Write-Host "✅ Fallback JPEG créé: $jpegPath" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Erreur lors de l'optimisation de $InputPath : $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Fonction pour optimiser les vidéos
function Optimize-Video {
    param(
        [string]$InputPath,
        [string]$OutputPath
    )
    
    try {
        # Vérifier si FFmpeg est disponible
        $ffmpegPath = Get-Command ffmpeg -ErrorAction SilentlyContinue
        if (-not $ffmpegPath) {
            Write-Host "⚠️ FFmpeg non trouvé. Les vidéos ne seront pas optimisées." -ForegroundColor Yellow
            Write-Host "Installez FFmpeg depuis: https://ffmpeg.org/download.html" -ForegroundColor Yellow
            return
        }
        
        # Optimiser la vidéo avec FFmpeg
        ffmpeg -i $InputPath -c:v libx264 -crf 28 -c:a aac -b:a 128k -movflags +faststart $OutputPath -y
        Write-Host "✅ Vidéo optimisée: $InputPath -> $OutputPath" -ForegroundColor Green
        
        # Créer aussi une version WebM
        $webmPath = $OutputPath -replace '\.mp4$', '.webm'
        ffmpeg -i $InputPath -c:v libvpx-vp9 -crf 30 -c:a libopus -b:a 128k $webmPath -y
        Write-Host "✅ Version WebM créée: $webmPath" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Erreur lors de l'optimisation de $InputPath : $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Optimiser toutes les images
Write-Host "🖼️ Optimisation des images..." -ForegroundColor Blue
$imageFiles = Get-ChildItem "images\*.jpg", "images\*.png" -ErrorAction SilentlyContinue

foreach ($image in $imageFiles) {
    $outputPath = "optimized\images\$($image.BaseName).webp"
    Optimize-Image -InputPath $image.FullName -OutputPath $outputPath
}

# Optimiser la vidéo principale (prendre la plus petite)
Write-Host "🎥 Optimisation des vidéos..." -ForegroundColor Blue
$videoFiles = Get-ChildItem "video\*.mp4" | Sort-Object Length
$mainVideo = $videoFiles[0]

if ($mainVideo) {
    $outputPath = "optimized\video\hero-video-optimized.mp4"
    Optimize-Video -InputPath $mainVideo.FullName -OutputPath $outputPath
}

# Créer un poster pour la vidéo
if ($mainVideo) {
    $posterPath = "optimized\images\video-poster.jpg"
    magick $mainVideo.FullName[0] -vf "select=eq(n\,0)" -vframes 1 -q:v 2 $posterPath
    Write-Host "✅ Poster vidéo créé: $posterPath" -ForegroundColor Green
}

# Générer un rapport de compression
Write-Host "`n📊 Rapport de compression:" -ForegroundColor Cyan

$originalSize = (Get-ChildItem "images", "video" -Recurse | Measure-Object -Property Length -Sum).Sum
$optimizedSize = (Get-ChildItem "optimized" -Recurse | Measure-Object -Property Length -Sum).Sum

if ($originalSize -gt 0) {
    $savings = $originalSize - $optimizedSize
    $percentage = [math]::Round(($savings / $originalSize) * 100, 2)
    
    Write-Host "Taille originale: $([math]::Round($originalSize / 1MB, 2)) MB" -ForegroundColor White
    Write-Host "Taille optimisée: $([math]::Round($optimizedSize / 1MB, 2)) MB" -ForegroundColor White
    Write-Host "Économie: $([math]::Round($savings / 1MB, 2)) MB ($percentage%)" -ForegroundColor Green
}

Write-Host "`n🎉 Optimisation terminée!" -ForegroundColor Green
Write-Host "Les fichiers optimisés sont dans le dossier 'optimized'" -ForegroundColor Blue
Write-Host "Remplacez les fichiers originaux par les versions optimisées" -ForegroundColor Yellow

