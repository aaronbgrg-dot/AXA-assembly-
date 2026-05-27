const cookieBox = document.querySelector(".wrapper"),
buttons = document.querySelectorAll(".button");


const executeCodes = () => {
    // si el usuario ya ha guardado las cookies anteriormente no se ejecuta 
    if(document.cookie.includes("codinglab")) return
    cookieBox.classList.add("show");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            cookieBox.classList.remove( "show");

            if (button.id == "Btn_aceptar"){
                // establecer cookies para 3 dias
                document.cookie = "cookieBy= codinglab; max-age=" + 60 * 60 * 24 * 3
            }
        })
    })
};

//se llamara a la funcion cuando la pagina cargue
window.addEventListener("load", executeCodes);