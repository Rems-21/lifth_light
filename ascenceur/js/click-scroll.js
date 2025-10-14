//jquery-click-scroll
//by syamsul'isul' Arifin

// Vérifier si les sections existent avant d'exécuter le script
$(document).ready(function(){
    // Fonction pour vérifier si un élément existe
    function elementExists(selector) {
        return $(selector).length > 0;
    }
    
    // Fonction pour obtenir l'offset en toute sécurité
    function getOffset(element) {
        if (element && element.length > 0) {
            return element.offset().top - 83;
        }
        return 0;
    }
    
    // Gérer les clics sur les liens de navigation
    $('.click-scroll').click(function(e){
        e.preventDefault();
        var target = $(this).attr('href');
        if (target && target.startsWith('#')) {
            var targetElement = $(target);
            if (targetElement.length > 0) {
                var offsetClick = getOffset(targetElement);
                $('html, body').animate({
                    'scrollTop': offsetClick
                }, 300);
            }
        }
    });
    
    // Gérer le scroll pour les sections existantes
    $(document).scroll(function(){
        var docScroll = $(document).scrollTop();
        var docScroll1 = docScroll + 1;
        
        // Vérifier chaque section possible
        var sections = ['#section_1', '#section_2', '#section_3', '#section_4', '#section_5', '#section_6'];
        
        sections.forEach(function(sectionId, index) {
            if (elementExists(sectionId)) {
                var offsetSection = getOffset($(sectionId));
                
                if (docScroll1 >= offsetSection) {
                    $('.navbar-nav .nav-item .nav-link').removeClass('active');
                    $('.navbar-nav .nav-item .nav-link').eq(index).addClass('active');
                }
            }
        });
    });
    
    // Initialiser les classes
    $('.navbar-nav .nav-item .nav-link').removeClass('active inactive');
    $('.navbar-nav .nav-item .nav-link').eq(0).addClass('active');
});