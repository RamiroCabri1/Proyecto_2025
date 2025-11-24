import { apiGet, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-clientes.js cargado y conectado al Backend.");

    const tablaBody = document.getElementById("clientes-body");
    
    // Función para llenar la tabla con datos
    function renderTabla(clientes) {
        tablaBody.innerHTML = "";

        clientes.forEach(cliente => {
            const fila = document.createElement("tr");

            //  devuelve: nombre, apellido, email, dni, telefono.
            // La tabla pide Servicio y Horario, pero eso está en otra tabla (Turnos).
            // Por ahora mostramos los datos del cliente y dejamos guiones en lo demás.
            
            fila.innerHTML = `
                <td>${cliente.nombre} ${cliente.apellido || ''}</td>
                <td>${cliente.email || 'Sin email'}</td>
                <td>${cliente.telefono}</td> 
                <td>-</td> 
                <td>
                    <button class="btn-cancelar" data-id="${cliente.id}">
                        Eliminar
                    </button>
                </td>
            `;

            tablaBody.appendChild(fila);
        });

        activarBotonesCancelar();
    }

    // Acción del botón eliminar
    function activarBotonesCancelar(){
        const botones = document.querySelectorAll(".btn-cancelar");

        botones.forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const id = e.target.dataset.id;
                
                if(confirm(`¿Seguro querés eliminar al cliente ID ${id}?`)) {
                    try {
                        // Llamada real al backend
                        const res = await apiDelete(`/clientes/${id}`);
                        
                        if (res.status === 200) {
                            alert("Cliente eliminado correctamente");
                            cargarClientes(); // Recargamos la tabla para ver el cambio
                        } else {
                            alert("Error al eliminar: " + (res.data.error || "Desconocido"));
                        }
                    } catch (error) {
                        console.error("Error:", error);
                    }
                }
            });
        });  
    }

    // Carga inicial
    async function cargarClientes(){
        console.log("Pidiendo clientes al Backend...");
        
        try {
            // Usamos la función del core que ya maneja el token
            const res = await apiGet("/clientes");

            if (res.status === 200) {
                console.log("Clientes recibidos:", res.data);
                renderTabla(res.data);
            } else {
                // Si el token venció (401), api.js o el usuario deberían manejarlo
                console.error("Error cargando clientes:", res);
                tablaBody.innerHTML = `<tr><td colspan="5">Error al cargar datos: ${res.status}</td></tr>`;
            }
        } catch (error) {
            console.error("Error grave:", error);
        }
    }
    cargarClientes();

});
