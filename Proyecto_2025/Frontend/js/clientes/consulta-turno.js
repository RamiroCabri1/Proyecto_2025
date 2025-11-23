import { apiGet } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("consulta-turno.js cargado correctamente ✔");

    const form = document.getElementById("form-consulta-turno");
    const inputCodigo = document.getElementById("codigo");
    const mensajeError = document.getElementById("mensaje-error");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const codigoIngresado = inputCodigo.value.trim();

        if (!codigoIngresado) {
            mensajeError.textContent = "Ingresá un código válido.";
            return;
        }

        // buscamos turno x codigo
        const res = await apiGet(`/turnos?codigo=${codigoIngresado}`);

        if (!res.ok || res.error || !res.data?.length) {
            mensajeError.textContent = "No se encontró ningún turno con ese código.";
            return;
        }

        const turno = res.data[0];

        // Guardar en localStorage para usarlo en detalles
        localStorage.setItem("turnoEnProceso", JSON.stringify(turno));

        // Redirigir a la pantalla de detalle
        window.location.href = "./clientes-turno-detalle.html";
    });
});
