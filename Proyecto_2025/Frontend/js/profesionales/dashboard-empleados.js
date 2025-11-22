import { apiGet, apiPost, apiDelete, apiPut } from "../core/api.js"

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-empleados.js cargado.");

    const tablaBody = document.getElementById("tabla-empleados").querySelector("tbody");

    //Botones/modales
    const btnAgregar = document.getElementById("btn-agregar-empleado");
    const modal = document.getElementById("modal-empleado");
    const modalConfirm = document.getElementById("modal-confirmacion");
    const btnCerrarModal = document.getElementById("cerrar-modal-empleado");
    const btnCancelarEliminar = document.getElementById("cancelar-eliminar");
    const btnConfirmarEliminar = document.getElementById("confirmar-eliminar");
    const formEmpleado = document.getElementById("form-empleado");

    let profesionalAEliminar = null;

    const NEGOCIO_ID = localStorage.getItem("negocio_id");

    if (!NEGOCIO_ID) {
        console.error("No se encontró negocio_id en localStorage.");
        alert("Error al cargar negocio.");
        return;
    }

    function renderTabla(lista){
    tablaBody.innerHTML = "";
    
    lista.forEach(prof =>{
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${prof.nombre}</td>
            <td>${prof.activo ? "Sí" : "No"}</td>
            <td>
                <button class="accion-eliminar" data-id="${prof.id}">Eliminar</button>
            </td>
        `;

        tablaBody.appendChild(fila);
    });

    activarEventosEliminar();
}


    // Cargar profesionales reales
    async function cargarProfesionales() {
        console.log("Cargando profesionales...");

        const res = await apiGet("/profesionales");

        if (!res.ok || res.error) {
            console.error("Error cargando profesionales:", res.error);
            return;
        }

        // Filtrar por negocio del usuario logueado
        const filtrados = res.filter(p => p.negocio_id == NEGOCIO_ID);

        renderTabla(filtrados);
    }

    // Modal p crear profesional
    btnAgregar.addEventListener("click", () => {
        modal.style.display = "block";
    });

    btnCerrarModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Guardar profesional nuevo
    formEmpleado.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nombre = document.getElementById("nombre-empleado").value.trim();

        if (!nombre) {
            alert("El nombre es obligatorio");
            return;
        }

        const payload = {
            nombre,
            negocio_id: Number(NEGOCIO_ID)
        };

        const res = await apiPost("/profesionales", payload);

        if (!res.ok || res.error) {
            console.error("Error creando profesional:", res.error);
            alert("No se pudo crear el profesional");
            return;
        }

        modal.style.display = "none";
        formEmpleado.reset();
        cargarProfesionales();
    });

    // Eliminar profesional
    function activarEventosEliminar() {
        const botones = document.querySelectorAll(".accion-eliminar");

        botones.forEach(btn => {
            btn.addEventListener("click", () => {
                profesionalAEliminar = btn.dataset.id;
                modalConfirm.style.display = "block";
            });
        });
    }

    btnCancelarEliminar.addEventListener("click", () => {
        modalConfirm.style.display = "none";
        profesionalAEliminar = null;
    });

    btnConfirmarEliminar.addEventListener("click", async () => {
        if (!profesionalAEliminar) return;

        const res = await apiDelete(`/profesionales/${profesionalAEliminar}`);

        if (!res.ok || res.error) {
            alert("No se pudo eliminar el profesional");
            return;
        }

        modalConfirm.style.display = "none";
        cargarProfesionales();
    });

    cargarProfesionales();
});