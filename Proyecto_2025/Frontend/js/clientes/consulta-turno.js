import { apiGet } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("consulta-turno.js cargado.");

    const form = document.querySelector("form"); 
    
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const inputCodigo = document.querySelector("input[type='text']"); 
            const codigoIngresado = inputCodigo.value.trim();

            if (!codigoIngresado) {
                alert("Ingresá un código válido.");
                return;
            }

            try {
                // preguntamos a la BD si existe
                const res = await apiGet(`/turnos/${codigoIngresado}`, false);

                if (res.status === 200) {
                    
                    // vamos a compartir el turno
                    localStorage.setItem("turnoCreadoId", codigoIngresado);
                    
                    // reutilizamos la pagina de detalle turno
                    window.location.href = "clientes-turno-detalle.html";
                } else {
                    alert("No se encontró ningún turno con ese código.");
                }

            } catch (error) {
                console.error(error);
                alert("Error de conexión.");
            }
        });
    }
});