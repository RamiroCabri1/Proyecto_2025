import { apiGet } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("consulta-turno.js cargado.");

    const form = document.getElementById("form-consulta-turno");
    const inputCodigo = document.getElementById("codigo");
    const mensajeError = document.getElementById("mensaje-error");

    if(form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            // Limpiamos el ID: si el usuario pone "TUR-5", nos quedamos solo con "5"
            let codigoIngresado = inputCodigo.value.trim();
            if (codigoIngresado.toUpperCase().startsWith("TUR-")) {
                codigoIngresado = codigoIngresado.replace("TUR-", "");
            }

            if (!codigoIngresado) {
                if(mensajeError) mensajeError.textContent = "Ingresá un código válido.";
                return;
            }

            try {
                // 1. Preguntamos a la BD si existe (Endpoint Público)
                const res = await apiGet(`/turnos/${codigoIngresado}`, false);

                if (res.status === 200) {
                    
                    // 2. Guardamos SOLO el ID en la caja compartida "turnoCreadoId"
                    localStorage.setItem("turnoCreadoId", codigoIngresado);
                    
                    // 3. Viajamos a la página de detalle
                    window.location.href = "clientes-turno-detalle.html";
                } else {
                    if(mensajeError) mensajeError.textContent = "No se encontró ningún turno con ese código.";
                    else alert("Turno no encontrado");
                }

            } catch (error) {
                console.error(error);
                alert("Error de conexión.");
            }
        });
    }
});