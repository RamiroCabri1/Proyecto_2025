import { apiGet, apiPost, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () =>{
    console.log("dashboard-servicios.js cargado.");
    
    const tablaBody = document.getElementById("servicios-body");

    const btnAbrirModal = document.getElementById("btn-agregar-servicio");
    const modal = document.getElementById("modal-servicio");
    const btnCerrarModal = document.getElementById("cerrar-modal");
    const formServicio = document.getElementById("form-servicio");

    //servicios de pruebita
    const serviciosMock = [
        {
            id: 1,
            nombre: "Masaje relajante",
            duracion: 45,
            precio: 8000
        },
        {
            id: 2,
            nombre: "Depilación facial",
            duracion: 30,
            precio: 5000
        }
    ];

    // reenderizar tabla
    function renderTabla(servicios){
        tablaBody.innerHTML = "";

        servicios.forEach(servicio => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
            <td>${servicio.nombre}</td>
            <td>${servicio.duracion} min</td>
            <td>$${servicio.precio}</td>
            <td>
                <a href="#" class="accion-cancelar" data-id="${servicio.id}">Eliminar</a>
            </td>
        `;

        tablaBody.appendChild(fila);
        });
    }

    function abrirModal(){
        modal.style.display = "block";
    }

    function cerrarModal(){
        modal.style.display="none";
    }

    //guardar servicio nuevo
    formServicio.addEventListener("submit", (e) =>{
        e.preventDefault();

        const nombre = document.getElementById("nombre-servicio").value.trim();
        const descripcion = document.getElementById("descripcion-servicio").value.trim();
        const duracion = parseInt(document.getElementById("duracion-servicio").value);


        //creamos un nuevo servicio (de mentiritas)
        const nuevoServicio = {
            id: Date.now(),
            nombre, 
            duracion,
            precio: 0
        }

        //Agregamos al array de mentiritas
        serviciosMock.push(nuevoServicio)
        
        // refresh tabla
        renderTabla(serviciosMock);

        //cerramos modal
        cerrarModal();

        //limpiar formulario
        formServicio.reset();

        //mensaje de exitoooo
        alert("Servicio agregado (de mentiritas)");
    });

    btnAbrirModal.addEventListener("click", abrirModal);
    btnCerrarModal.addEventListener("click", cerrarModal);

    //cargar tabla
    renderTabla(serviciosMock);
});