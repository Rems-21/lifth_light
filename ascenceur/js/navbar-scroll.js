// Script pour unifier le comportement de la navbar au défilement
$(document).ready(function() {
    // Fonction pour gérer le scroll
    function handleNavbarScroll() {
        var scrollTop = $(window).scrollTop();
        var navbar = $('.navbar');
        
        if (scrollTop > 50) {
            navbar.addClass('scrolled');
        } else {
            navbar.removeClass('scrolled');
        }
    }
    
    // Écouter le scroll
    $(window).on('scroll', handleNavbarScroll);
    
    // Vérifier l'état initial
    handleNavbarScroll();
});
