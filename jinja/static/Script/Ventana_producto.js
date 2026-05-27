const abrir_producto_completo = document.querySelector("#abrir_producto_completo");
const ver_producto_completo = document.querySelector("#ver_producto_completo");
const cerrar_ventana_producto = document.querySelector("#cerrar_ventana_producto");


abrir_producto_completo.addEventListener("click", ()=>{
    ver_producto_completo.showModal();
})

cerrar_ventana_producto.addEventListener("click", ()=>{
    ver_producto_completo.close();
})