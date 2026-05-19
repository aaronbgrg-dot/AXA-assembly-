// ── Carrusel de anuncios ──
    function Cargar_carrusel_Anuncios() {
        const anuncios = document.querySelectorAll('.anuncio');
        const contenedorPuntos = document.getElementById('carruselPuntos');
        let actual = 0;

        
        anuncios.forEach((_, i) => {});

        function irA(indice) {
            anuncios[actual].classList.remove('activo');;
            actual = indice % anuncios.length;
            anuncios[actual].classList.add('activo');
        }

        // Cambio automático cada 10 segundos
        setInterval(() => irA(actual + 1), 10000);
    };

    function Menu_login_registro() {
        const menu = document.getElementById("menuLogin");
        //ayuda de la IA para saber como poner el dropdown solo cuando el usuario haga click en el icono
        menu.style.display = (menu.style.display === "block") ? "none" : "block";
    }