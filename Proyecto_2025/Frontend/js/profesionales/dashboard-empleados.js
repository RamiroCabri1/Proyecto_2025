import { apiGet, apiPost, apiDelete } from "../core/api.js"

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

    //Mock de empleados
    const empleadosMock = [
        {
            id: 1,
            nombre: "Laura Gómez",
            puesto: "Maquilladora",
            email: "laura@empresa.com",
            activo: true
        },
        {
            id: 2,
            nombre: "Marcos Díaz",
            puesto: "Masajista",
            email: "marcos@empresa.com",
            activo: true
        }
    ]; 

    //renderizar tabla
    function renderTabla(empleados){
        tablaBody.innerHTML = "";
        
        empleados.forEach(empleado =>{
            const fila = document.createElement("tr");

            fila.innerHTML = `
            <td>${empleado.nombre}</td>
            <td>${empleado.puesto}</td>
            <td>${empleado.email}</td>
            <td>${empleado.activo ? "Sí" : "No"}</td>
            <td>
                <a href="#" class="accion-editar" data-id="${empleado.id}">Editar</a> |
                <a href="#" class="accion-cancelar" data-id="${empleado.id}">Eliminar</a>
            </td>
        `;

        tablaBody.appendChild(fila);
        })
    }

    //abrir y cerrar modal
    function abrirModal(){
        modal.style.display = "block";
    }

    function cerrarModal(){
        modal.style.display = "none";
    }

    //eventos
    btnAgregar.addEventListener("click", abrirModal);
    btnCerrarModal.addEventListener("click", cerrarModal);

    //render inicial
    renderTabla(empleadosMock);
    
});