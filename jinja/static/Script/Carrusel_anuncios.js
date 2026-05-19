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