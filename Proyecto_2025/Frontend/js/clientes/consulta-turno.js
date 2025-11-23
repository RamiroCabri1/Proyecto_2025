import { apiGet, apiPut } from "../core/api.js";


document.addEventListener("DOMContentLoaded", async () => {
    console.log("consultar-turno.js cargado.");

    //leer el ID del turno, lo sacamos de localstorage
    const turnoGuardado = JSON.parse(localStorage.getItem("turnoEnProceso"));
    if (!turnoGuardado) {
        alert("No se encontró información del turno.");
        window.location.href = "./clientes-turno.html";
        return;
    }

    const turno_id = turnoGuardado.id;


    // Pedimos turno a backend
    const resTurno = await apiGet(`/turnos?id=${turno_id}`);

    if (!resTurno.ok || resTurno.error || !resTurno.data?.length) {
        alert("No se pudo obtener los datos del turno.");
        console.error("Error turno:", resTurno);
        return;
    }

    const turno = resTurno.data[0];

    // Moidificado. Toda la seccion mock reemplazada para que pida datos reales

    
    document.getElementById("codigo-turno").textContent =
        turnoGuardado.codigo || "-";
    //datos reales del turno mostramos ya me olvide de como hablar
    document.getElementById("cliente-nombre").textContent = turno.cliente_nombre;
    document.getElementById("profesional-nombre").textContent = turno.profesional_nombre;
    document.getElementById("servicio-nombre").textContent = turno.servicio_nombre;

    //backend devuelve fehca y hora
    const [fechaReal, horaReal] = turno.fecha_hora.split(" ");

    document.getElementById("turno-fecha").textContent = fechaReal;  
    document.getElementById("turno-horario").textContent = horaReal;  

    document.getElementById("estado-turno").textContent = turno.estado;

    // Cancelar turno

    const btnCancelar = document.querySelector(".btn.cancelar");

    btnCancelar.addEventListener("click", async () => {
        const confirmacion = confirm("¿Seguro que querés cancelar el turno?");

        if (!confirmacion) return;

        const resCancel = await apiPut(`/turnos?id=${turno_id}`, { estado: "Cancelado" });

        if (!resCancel.ok || resCancel.error) {
            alert("No se pudo cancelar el turno.");
            console.error(resCancel);
            return;
        }

        const actualizado = { 
            ...turnoGuardado, 
            estado: "Cancelado"
        };

        localStorage.setItem("turnoEnProceso", JSON.stringify(actualizado));

        alert("Tu turno fue cancelado.");
    });

});