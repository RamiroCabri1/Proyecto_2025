import { apiGet, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-clientes.js cargado.");

    const tablaBody = document.getElementById("clientes-body");
    const NEGOCIO_ID = localStorage.getItem("negocio_id") || 1; 

    //datos mockup a cambiar cuando conectemos con backuppppp

    const clientesFalsos = [
        {
            id: 1,
            nombre: "Ana Maria",
            email: "ana@gmail.com",
            servicio: "masaje",
            horario: "10:00"
        },
        {
            id: 2, 
            nombre: "Juan Jose",
            email: "juan@gmail.com",
            servicio: "lifting",
            horario: "11:00"
        }
    ];

    //funcion llenar tabla
    function renderTabla(clientes) {
        tablaBody.innerHTML = "";

        clientes.forEach(cliente => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${cliente.nombre}</td>
                <td>${cliente.email}</td>
                <td>${cliente.servicio}</td>
                <td>${cliente.horario}</td>
                <td>
                    <button class="btn-cancelar" data-id="${cliente.id}">
                        Cancelar
                    </button>
                </td>
            `;

            tablaBody.appendChild(fila);
        });


        activarBotonesCancelar();
    
    }

    //accion cancelr turno 

    function activarBotonesCancelar(){
        const botones = document.querySelectorAll(".btn-cancelar");

        botones.forEach(btn =>{
            btn.addEventListener("click",(e) => {
                const id = e.target.dataset.id;
                //para cambiar dsps
                alert(`Cancelando turno ID ${id} (falso por ahora)`);
            });
        });  
    }


    //simulamos carga inicial
    function cargarClientes(){
        console.log("Cargando clientes de mentiritas");
        renderTabla(clientesFalsos);
    }

    cargarClientes();

});

