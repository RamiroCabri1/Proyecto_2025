import { apiGet, apiPost, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-servicios.js cargado.");
    
    const tablaBody = document.getElementById("servicios-body");

    const btnAbrirModal = document.getElementById("btn-agregar-servicio");
    const modal = document.getElementById("modal-servicio");
    const btnCerrarModal = document.getElementById("cerrar-modal");
    const formServicio = document.getElementById("form-servicio");

    // Función para llenar la tabla con datos reales (Osea digamos mi base de datos)
    function renderTabla(servicios){
        tablaBody.innerHTML = "";

        servicios.forEach(servicio => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
            <td>${servicio.nombre}</td>
            <td>${servicio.duracion_turno_min} min</td>
            <td>${servicio.descripcion || '-'}</td> 
            <td>
                <a href="#" class="accion-cancelar" data-id="${servicio.id}" style="color: red; font-weight: bold;">Eliminar</a>
            </td>
        `;

        tablaBody.appendChild(fila);
        });

        // Conectamos los botones recién creados
        activarBotonesEliminar();
    }

    // Función para activar los clics de eliminar
    function activarBotonesEliminar() {
        const botones = document.querySelectorAll(".accion-cancelar");

        botones.forEach(btn => {
            btn.addEventListener("click", async (e) => {
                e.preventDefault(); // Evita que salte la página
                const id = e.target.dataset.id;

                if(confirm(`¿Seguro que querés eliminar el servicio ID ${id}?`)) {
                    try {
                        const res = await apiDelete(`/servicios/${id}`);
                        
                        if (res.status === 200) {
                            alert("Servicio eliminado correctamente.");
                            cargarServicios(); // Recargamos la tabla
                        } else {
                            alert("Error al eliminar: " + (res.data.error || "Desconocido"));
                        }
                    } catch (error) {
                        console.error("Error eliminando:", error);
                    }
                }
            });
        });
    }

    // Función ASYNC para pedir los datos al Backend
    async function cargarServicios() {
        try {
            const res = await apiGet("/servicios");

            if (res.status === 200) {
                renderTabla(res.data);
            } else {
                console.error("Error:", res);
            }
        } catch (error) {
            console.error("Error grave:", error);
        }
    }
function abrirModal(){
        console.log("¡Hiciste clic en el botón!");
        modal.style.display = "block";
    }

    function cerrarModal(){
        modal.style.display="none";
    }

// Lógica de crear servicio
    if(formServicio) {
        formServicio.addEventListener("submit", async (e) => {
            e.preventDefault(); // Frenamos el recargo de página

            // Capturamos los datos usando los IDs que encontramos
            const nombre = document.getElementById("nombre-servicio").value.trim();
            const descripcion = document.getElementById("descripcion-servicio").value.trim();
            const duracion = document.getElementById("duracion-servicio").value;
            
            // Obtenemos el ID del negocio (o usamos el 6 que es el mio)
            const negocio_id = localStorage.getItem("negocio_id") || 6;

            // Armamos el paquete para Python
            const nuevoServicio = {
                nombre: nombre,
                descripcion: descripcion,
                duracion_turno_min: parseInt(duracion),
                negocio_id: parseInt(negocio_id)
            };

            try {
                // Enviamos el paquete
                const res = await apiPost("/servicios", nuevoServicio);

                if (res.status === 201) { 
                    alert("Servicio creado con éxito");
                    
                    cerrarModal();
                    formServicio.reset(); // Limpiamos el formulario
                    cargarServicios();    // Recargamos la tabla para ver el nuevo
                } else {
                    alert("Error al crear: " + (res.data.error || "Verificá los datos"));
                }
            } catch (error) {
                console.error(error);
                alert("Error de conexión");
            }
        });
    }

if(btnAbrirModal) btnAbrirModal.addEventListener("click", abrirModal);
    if(btnCerrarModal) btnCerrarModal.addEventListener("click", cerrarModal);
    
    // Ejecutamos
    cargarServicios();
});