import { apiGet, apiPost, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-servicios.js cargado.");
    
    const tablaBody = document.getElementById("servicios-body");
    const btnAbrirModal = document.getElementById("btn-agregar-servicio");
    const modal = document.getElementById("modal-servicio");
    const btnCerrarModal = document.getElementById("cerrar-modal");
    const formServicio = document.getElementById("form-servicio");

    // --- 1. CARGAR (GET) ---
    async function cargarServicios() {
        try {
            const res = await apiGet("/servicios"); // Pide al backend

            if (res.status === 200) {
                renderTabla(res.data); // Dibuja lo que viene del backend
            } else {
                console.error("Error cargando servicios:", res);
            }
        } catch (error) {
            console.error("Error critico:", error);
        }
    }

    function renderTabla(servicios){
        // Si no hay tbody, salimos
        if (!tablaBody) return;
        
        tablaBody.innerHTML = "";

        servicios.forEach(servicio => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
            <td>${servicio.nombre}</td>
            <td>${servicio.duracion_turno_min} min</td>
            <td>${servicio.descripcion || '-'}</td> 
            <td>
                <a href="#" class="accion-cancelar" data-id="${servicio.id}" style="color: red; font-weight: bold; cursor: pointer;">Eliminar</a>
            </td>
        `;
        tablaBody.appendChild(fila);
        });

        activarBotonesEliminar();
    }

    // --- 2. ELIMINAR (DELETE) ---
    function activarBotonesEliminar() {
        const botones = document.querySelectorAll(".accion-cancelar");
        botones.forEach(btn => {
            btn.addEventListener("click", async (e) => {
                e.preventDefault();
                const id = e.target.dataset.id;
                if(confirm(`¿Eliminar servicio ID ${id}?`)) {
                    const res = await apiDelete(`/servicios/${id}`);
                    if (res.status === 200) cargarServicios();
                    else alert("Error al eliminar");
                }
            });
        });
    }

    // --- 3. CREAR (POST) ---
    if(formServicio) {
        formServicio.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            // IDs del HTML (Asegurate que coincidan)
            const nombre = document.getElementById("nombre-servicio").value;
            // Si tu html dice precio-servicio cambialo acá:
            const descripcion = document.getElementById("descripcion-servicio") ? document.getElementById("descripcion-servicio").value : "-";
            const duracion = document.getElementById("duracion-servicio").value;
            
            const negocio_id = localStorage.getItem("negocio_id") || 6;

            const nuevoServicio = {
                nombre: nombre,
                descripcion: descripcion,
                duracion_turno_min: parseInt(duracion),
                negocio_id: parseInt(negocio_id)
            };

            const res = await apiPost("/servicios", nuevoServicio);

            if (res.status === 201) {
                alert("Creado correctamente");
                modal.style.display = "none";
                formServicio.reset();
                cargarServicios();
            } else {
                alert("Error: " + (res.data.error || "Revisá los datos"));
            }
        });
    }

    // --- MODAL ---
    if(btnAbrirModal) btnAbrirModal.onclick = () => { if(modal) modal.style.display = "block"; };
    if(btnCerrarModal) btnCerrarModal.onclick = () => { if(modal) modal.style.display = "none"; };

    // INICIALIZAR
    cargarServicios();
});