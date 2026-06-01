// ── Carrusel de anuncios ──
function Cargar_carrusel_Anuncios() {
    const anuncios = document.querySelectorAll('.anuncio');
    const contenedorPuntos = document.getElementById('carruselPuntos');
    
    // En vez de empezar en 0, busca el índice del anuncio activo
    let actual = Array.from(anuncios).findIndex(anuncio => anuncio.classList.contains('activo'));
    if (actual === -1) actual = 0; // Por si acaso ninguno tuviera la clase, empieza en 0

    anuncios.forEach((_, i) => {});

    function irA(indice) {
        anuncios[actual].classList.remove('activo');
        actual = indice % anuncios.length;
        anuncios[actual].classList.add('activo');
    }

    // Cambio automático cada 10 segundos
    setInterval(() => irA(actual + 1), 10000);
};