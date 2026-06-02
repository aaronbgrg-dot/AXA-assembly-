

const carrito = {};


function agregarCarrito(btn) {

    const id = Number(btn.dataset.id);
    const nombre = btn.dataset.nombre;
    const precio = Number(btn.dataset.precio);

    if (!carrito[id]) {
        carrito[id] = {
            id: id,
            nombre: nombre,
            precio: precio,
            cantidad: 1
        };
    } else {
        carrito[id].cantidad++;
    }

    renderCarrito();
}


function aumentar(id) {

    id = Number(id);

    if (carrito[id]) {
        carrito[id].cantidad++;
        renderCarrito();
    }
}


function disminuir(id) {

    id = Number(id);

    if (!carrito[id]) return;

    carrito[id].cantidad--;

    if (carrito[id].cantidad <= 0) {
        delete carrito[id];
    }

    renderCarrito();
}


function renderCarrito() {

    const contenedor = document.getElementById("productos-carrito");
    const totalSpan = document.getElementById("total-carrito");
    const contador = document.getElementById("contador-carrito");

    if (!contenedor || !totalSpan || !contador) return;

    const items = Object.values(carrito);

    let html = "";
    let total = 0;
    let cantidadTotal = 0;

    if (items.length === 0) {
        contenedor.innerHTML = "<p>Carrito vacío</p>";
        totalSpan.innerText = "0.00 €";
        contador.innerText = "🛒 0";
        return;
    }

    items.forEach(p => {

        const subtotal = p.precio * p.cantidad;

        total += subtotal;
        cantidadTotal += p.cantidad;

        html += `
            <div class="item-carrito">
                <strong>${p.nombre}</strong><br>
                ${p.precio.toFixed(2)} € x ${p.cantidad}<br>
                <small>Subtotal: ${subtotal.toFixed(2)} €</small><br>

                <button type="button" onclick="disminuir(${p.id})">-</button>
                <button type="button" onclick="aumentar(${p.id})">+</button>
            </div>
            <hr>
        `;
    });

    contenedor.innerHTML = html;
    totalSpan.innerText = total.toFixed(2) + " €";
    contador.innerText = "🛒 " + cantidadTotal;
}


function mostrarCarrito(event) {

    if (event) event.preventDefault();

    const menu = document.getElementById("menuCarrito");

    if (!menu) return;

    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

document.addEventListener("DOMContentLoaded", () => {
    renderCarrito();
});