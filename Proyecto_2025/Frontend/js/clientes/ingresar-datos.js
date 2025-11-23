import { apiGet, apiPost, apiPut } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("ingresar-datos.js cargado");

    const form = document.getElementById("form-datos-turno");

    const params = new URLSearchParams(window.location.search);

    const profesional_id = params.get("profesional_id");
    const servicio_id = params.get("servicio_id");
    const horario = params.get("horario");
    const fecha = params.get("fecha");
    const negocio_id = params.get("negocio_id");

    // Guardar valores ocultos
    document.getElementById("profesional_id").value = profesional_id;
    document.getElementById("servicio_id").value = servicio_id;
    document.getElementById("horario").value = horario;
    document.getElementById("negocio_id").value = negocio_id;
    document.getElementById("fecha").value = fecha;

    async function cargarResumen() {
    const profRes = await apiGet(`/profesionales?id=${profesional_id}`);
    const servRes = await apiGet(`/servicios?id=${servicio_id}`);

    const profesional = profRes.data?.[0]?.nombre || "Profesional";
    const servicio = servRes.data?.[0]?.nombre || "Servicio";

    const resumen = document.getElementById("resumen-turno");
    resumen.innerHTML = `
        Estás reservando con <strong>${profesional}</strong> para 
        <strong>${servicio}</strong> el día 
        <strong>${fecha} a las ${horario}</strong>.
    `;
}

cargarResumen();


    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // datos del cliente
        const nombre = document.getElementById("nombre").value.trim();
        const apellido = document.getElementById("apellido").value.trim();
        const dni = document.getElementById("dni").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const email = document.getElementById("email").value.trim();

         // Crear/actualizar cliente
        const clientePayload = {
            nombre,
            apellido,
            dni,
            telefono,
            email,
            negocio_id: Number(negocio_id)
        };

        const resCliente = await apiPut("/clientes", clientePayload);

        if (!resCliente.ok || resCliente.error) {
            alert("No se pudo registrar el cliente.");
            console.error(resCliente);
            return;
        }

        const cliente_id = resCliente.data?.id || resCliente.id;

        // Crear fecha_hora
        const fecha_hora = `${fecha} ${horario}`;
        
         // Crear turno
        const turnoPayload = {
            fecha_hora,
            cliente_id,
            profesional_id: Number(profesional_id),
            servicio_id: Number(servicio_id),
            negocio_id: Number(negocio_id)
        };

        const resTurno = await apiPost("/turnos", turnoPayload);

            if (!resTurno.ok || resTurno.error) {
                alert("No se pudo crear el turno.");
                console.error(resTurno);
                return;
            }

          // Guardamos para la pantalla final
        localStorage.setItem("turnoEnProceso", JSON.stringify(resTurno.data || resTurno));

        window.location.href = "./clientes-turno-detalle.html";
    });
});