import { apiGet, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    const tablaBody = document.querySelector("tbody"); 

    async function cargarTurnos() {
        try {
            // Pedimos los TURNOS (no los clientes)
            const res = await apiGet("/turnos");

            if (res.status === 200) {
                renderTabla(res.data);
            } else {
                console.error("Error:", res);
            }
        } catch (error) {
            console.error(error);
        }
    }

    function renderTabla(turnos) {
        tablaBody.innerHTML = "";
        
        // Fecha de hoy para comparar
        const ahora = new Date();

        turnos.forEach(turno => {
            // --- TU LÓGICA DE ESTADOS ---
            const fechaTurno = new Date(turno.fecha_hora); // Convierte string a fecha
            let estadoTexto = "Pendiente";
            let colorEstado = "orange";

            // Si la fecha del turno es menor a la actual, ya pasó.
            if (fechaTurno < ahora) {
                estadoTexto = "Realizado";
                colorEstado = "green";
            }

            // Formateo de fecha para que se vea linda (dd/mm hh:mm)
            const fechaLinda = fechaTurno.toLocaleString();

            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${turno.cliente_nombre}</td>
                <td>${turno.cliente_telefono}</td>
                <td>${turno.profesional_nombre}</td>
                <td>${fechaLinda}</td>
                <td style="color: ${colorEstado}; font-weight: bold;">${estadoTexto}</td>
                <td>
                    <button class="btn-borrar" data-id="${turno.id}" style="color: red; cursor: pointer;">Eliminar</button>
                </td>
            `;
            tablaBody.appendChild(fila);
        });

        activarBotonesBorrar();
    }

    function activarBotonesBorrar() {
        document.querySelectorAll(".btn-borrar").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const id = e.target.dataset.id;
                if (confirm("¿Eliminar este turno?")) {
                    await apiDelete(`/turnos/${id}`);
                    cargarTurnos();
                }
            });
        });
    }

    cargarTurnos();
});