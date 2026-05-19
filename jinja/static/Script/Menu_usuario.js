function Menu_login_registro() {
        const menu = document.getElementById("menuLogin");
        //ayuda de la IA para saber como poner el dropdown solo cuando el usuario haga click en el icono
        menu.style.display = (menu.style.display === "block") ? "none" : "block";
    }


    // Cerrar el menú si se hace clic fuera
  window.onclick = function(event) {
        if (!event.target.matches('.login')) {
            //Fin uso IA
            document.getElementById("menuLogin").style.display = "none";
        }
    }