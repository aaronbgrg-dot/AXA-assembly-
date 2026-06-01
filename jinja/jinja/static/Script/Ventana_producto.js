// const abrir_producto_completo = document.querySelector("#abrir_producto_completo");
// const ver_producto_completo = document.querySelector("#ver_producto_completo");
// const cerrar_ventana_producto = document.querySelector("#cerrar_ventana_producto");


// abrir_producto_completo.addEventListener("click", ()=>{
//     ver_producto_completo.showModal();
// })

// cerrar_ventana_producto.addEventListener("click", ()=>{
//     ver_producto_completo.close();
// })

document.addEventListener("DOMContentLoaded", function() {
    const tarjetas = document.querySelectorAll('.tarjeta-producto');
    
    tarjetas.forEach(tarjeta => {
        const botonAbrir = tarjeta.querySelector('.boton-abrir');
        const panelDetalle = tarjeta.querySelector('.producto-detallado');
        const botonCerrar = panelDetalle ? panelDetalle.querySelector('.boton-cerrar') : null;
        
        // Función para abrir la vista rápida
        if (botonAbrir && panelDetalle) {
            botonAbrir.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                panelDetalle.style.display = 'block'; // Lo muestra
            });
        }
        
        // Función para cerrar con el botón "Cerrar"
        if (botonCerrar && panelDetalle) {
            botonCerrar.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                panelDetalle.style.display = 'none'; // Lo oculta
            });
        }
        
        // Función para cerrar si hacen clic fuera del recuadro blanco
        if (panelDetalle) {
            panelDetalle.addEventListener('click', (e) => {
                // Si hacen clic en el fondo gris del modal (y no en el contenido)
                if (e.target === panelDetalle) {
                    panelDetalle.style.display = 'none';
                }
            });
        }
    });
});