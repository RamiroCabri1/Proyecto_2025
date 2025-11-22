import { apiGet, apiPost, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () =>{
    console.log("dashboard-servicios.js cargado.");
    
    const tablaBody = document.getElementById("servicios-body");

    const btnAbrirModal = document.getElementById("btn-agregar-servicio");
    const modal = document.getElementById("modal-servicio");
    const btnCerrarModal = document.getElementById("cerrar-modal");
    const formServicio = document.getElementById("form-servicio");

    const NEGOCIO_ID = localStorage.getItem("negocio_id");

    if (!NEGOCIO_ID) {
        alert("No se encontró negocio_id");
        return;
    }

    //abrir modal
    btnAbrirModal.addEventListener("click", () => {
        modal.style.display = "block";
    });

    // cerrar modal
    btnCerrarModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // reenderizar tabla
    function renderTabla(servicios){
        tablaBody.innerHTML = "";

        servicios.forEach(serv => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${serv.nombre}</td>
                <td>${serv.duracion_turno_min} min</td>
                <td>
                    <button class="btn-eliminar" data-id="${serv.id}">Eliminar</button>
                </td>
            `;

        tablaBody.appendChild(fila);
        });
        activarBotonesEliminar();
    }

    //cargar servicios

    async function cargarServicios() {
        const res = await apiGet("/servicios");

        if (!res.ok || res.error) {
            console.error("Error obteniendo servicios:", res.error);
            return;
        }

        const filtrados = res.filter(s => s.negocio_id == NEGOCIO_ID);

        renderTabla(filtrados);
    }


    //guardar servicio nuevo
    formServicio.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        nombre: document.getElementById("nombre-servicio").value.trim(),
        descripcion: document.getElementById("descripcion-servicio").value.trim(),
        duracion_turno_min: Number(document.getElementById("duracion-servicio").value),
        negocio_id: Number(NEGOCIO_ID)
    };

    const res = await apiPost("/servicios", payload);

    if (!res.ok || res.error) {
        alert("No se pudo crear el servicio");
        return;
    }

    modal.style.display = "none";
    formServicio.reset();
    cargarServicios();
});

    // Eliminar servicio
    function activarBotonesEliminar() {
        document.querySelectorAll(".btn-eliminar").forEach(btn => {
            btn.addEventListener("click", async () => {

                const confirmar = confirm("¿Eliminar este servicio?");
                if (!confirmar) return;

                const id = btn.dataset.id;

                const res = await apiDelete(`/servicios/${id}`);

                if (!res.ok || res.error) {
                    alert("No se pudo eliminar");
                    return;
                }

                cargarServicios();
            });
        });
    }

    // Inicio
    cargarServicios();
}); 