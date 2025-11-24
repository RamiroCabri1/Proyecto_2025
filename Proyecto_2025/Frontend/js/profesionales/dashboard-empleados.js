import { apiGet, apiPost, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-empleados.js cargado.");

    const tablaBody = document.getElementById("tabla-empleados").querySelector("tbody");

    // Botones y Modales
    const btnAgregar = document.getElementById("btn-agregar-empleado");
    const modal = document.getElementById("modal-empleado");
    const btnCerrarModal = document.getElementById("cerrar-modal-empleado");
    const formEmpleado = document.getElementById("form-empleado");

    //  CARGAR EMPLEADOS
    async function cargarEmpleados() {
        try {
            const res = await apiGet("/profesionales"); 
            
            if (res.status === 200) {
                renderTabla(res.data);
            } else {
                console.error("Error al cargar empleados:", res);
            }
        } catch (error) {
            console.error(error);
        }
    }

    function renderTabla(empleados){
        tablaBody.innerHTML = "";
        
        empleados.forEach(empleado => {
            const fila = document.createElement("tr");

            // La DB no tiene Puesto ni Email.
            // Ponemos "-" en esas columnas, en el html se ve pero no se guarda
            
            fila.innerHTML = `
                <td>${empleado.nombre}</td>
                <td>-</td> 
                <td>-</td> 
                <td>${empleado.activo ? "Sí" : "No"}</td>
                <td>
                    <a href="#" class="accion-cancelar" data-id="${empleado.id}" style="color: red; font-weight: bold;">Eliminar</a>
                </td>
            `;

            tablaBody.appendChild(fila);
        });

        activarBotonesEliminar();
    }

    // LIMINAR EMPLEADO
    function activarBotonesEliminar() {
        const botones = document.querySelectorAll(".accion-cancelar");
        
        botones.forEach(btn => {
            btn.addEventListener("click", async (e) => {
                e.preventDefault();
                const id = e.target.dataset.id;

                if(confirm(`¿Seguro que querés eliminar este empleado (ID ${id})?`)) {
                    try {
                        const res = await apiDelete(`/profesionales/${id}`);
                        
                        if(res.status === 200) {
                            alert("Eliminado correctamente.");
                            cargarEmpleados();
                        } else {
                            alert("Error al eliminar: " + (res.data.error || "Desconocido"));
                        }
                    } catch (error) {
                        console.error(error);
                    }
                }
            });
        });
    }

    //  CREAR EMPLEADO
    if(formEmpleado) {
        formEmpleado.addEventListener("submit", async (e) => {
            e.preventDefault();

            const nombre = document.getElementById("nombre-empleado").value;
            const activoSelect = document.getElementById("activo-empleado").value;
            
            // Convertimos el texto "true"/"false" a booleano real
            const activo = (activoSelect === "true");
            
            // Ignoramos los inputs de puesto y email del HTML
            // Por el momento ya que en la base de datos no tienen un lugar
            // Decidimos que solo se puede registrar el jefe
            
            const negocio_id = localStorage.getItem("negocio_id") || 6;

            const nuevoEmpleado = {
                nombre: nombre,
                activo: activo,
                negocio_id: parseInt(negocio_id)
            };

            try {
                const res = await apiPost("/profesionales", nuevoEmpleado);

                if (res.status === 201) {
                    alert("Empleado creado con éxito!");
                    cerrarModal();
                    formEmpleado.reset();
                    cargarEmpleados(); // Recargamos la tabla
                } else {
                    alert("Error: " + (res.data.error || "Revisá los datos"));
                }
            } catch (error) {
                console.error(error);
            }
        });
    }

    // Lógica Visual del Modal
    function abrirModal(){
        modal.style.display = "block";
    }

    function cerrarModal(){
        modal.style.display = "none";
    }

    if(btnAgregar) btnAgregar.addEventListener("click", abrirModal);
    if(btnCerrarModal) btnCerrarModal.addEventListener("click", cerrarModal);

    // Inicializamos
    cargarEmpleados();
});