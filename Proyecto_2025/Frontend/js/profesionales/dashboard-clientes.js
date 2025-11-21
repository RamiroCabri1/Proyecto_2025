import { apiGet, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-clientes.js cargado.");

    const tablaBody = document.getElementById("clientes-body");
    const NEGOCIO_ID = localStorage.getItem("negocio_id");

    if (!NEGOCIO_ID){

        console.error("No hay negocio_id");
        return;
    }

    //funcion llenar tabla
    function renderTabla(clientes) {
        tablaBody.innerHTML = "";

        clientes.forEach(cliente => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${cliente.nombre}</td>
                <td>${cliente.apellido || ""}</td>
                <td>${cliente.dni}</td>
                <td>${cliente.email || "-"}</td>
                <td>${cliente.telefono || "-"}</td>
                <td>
                    <button class="btn-eliminar" data-id="${cliente.id}">
                        Eliminar
                    </button>
                </td>
            `;
            tablaBody.appendChild(fila);
        });


        activarBotonesEliminar();
    
    }

    //accion eliminar cliente

    function activarBotonesEliminar(){
        const botones = document.querySelectorAll(".btn-eliminar");

        botones.forEach(btn =>{
            btn.addEventListener("click",async (e) => {
                const id = e.target.dataset.id;
                
                const confirmar = confirm("¿Seguro que deseas eliminar este cliente?");
                if (!confirmar) return;

                const res = await apiDelete(`/clientes/${id}`);

                if (!res.ok || res.error) {
                    alert("No se pudo eliminar el cliente");
                    console.error(res.error);
                    return;
                }

                cargarClientes();
            });
        });
    }


    //carga real
    async function cargarClientes() {
        console.log("Cargando clientes...");

        const res = await apiGet("/clientes");

        if (!res.ok || res.error) {
            console.error("Error cargando clientes:", res.error);
            return;
        }

        // Filtrar por negocio del usuario logueado
        const clientesFiltrados = res.filter(c => c.negocio_id == NEGOCIO_ID);

        renderTabla(clientesFiltrados);
    }

    cargarClientes();
});
    

