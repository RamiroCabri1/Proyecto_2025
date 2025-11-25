import { apiGet, apiPut } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("dashboard-ajustes.js cargado.");

    const form = document.getElementById("form-ajustes");

    // Inputs
    const inputNombre = document.getElementById("nombre-negocio");
    const inputTelefono = document.getElementById("telefono-negocio");
    const inputDireccion = document.getElementById("direccion-negocio");
    
    // Estos dos quedan de adorno por ahora (no están en la BD)
    const inputApertura = document.getElementById("hora-apertura");
    const inputCierre = document.getElementById("hora-cierre");

    let negocioIdReal = null;

    // --- 1. CARGAR DATOS REALES (GET) ---
    async function cargarDatos() {
        console.log("Consultando datos al Backend...");

        try {
            // Usamos el endpoint especial que mira el token para saber quién sos
            const res = await apiGet("/negocios/mi-negocio");

            if (res.status === 200) {
                const datos = res.data;
                negocioIdReal = datos.id; // Guardamos el ID para poder guardar después

                // Rellenar inputs con datos de la BD
                inputNombre.value = datos.nombre;
                inputTelefono.value = datos.telefono;
                inputDireccion.value = datos.direccion;

                // (Opcional) Si quisieras simular horarios:
                // inputApertura.value = "09:00";
                
            } else {
                console.error("Error cargando negocio:", res);
                alert("No se pudo cargar la información del negocio.");
            }
        } catch (error) {
            console.error(error);
        }
    }

    cargarDatos();

    // --- 2. GUARDAR CAMBIOS (PUT) ---
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            if (!negocioIdReal) {
                alert("Error: No se cargó el ID del negocio.");
                return;
            }

            const payload = {
                nombre: inputNombre.value.trim(),
                telefono: inputTelefono.value.trim(),
                direccion: inputDireccion.value.trim()
                // No enviamos hora_apertura ni cierre porque la BD no los tiene
            };

            console.log("Enviando cambios...", payload);

            try {
                const res = await apiPut(`/negocios/${negocioIdReal}`, payload);

                if (res.status === 200) {
                    alert("¡Cambios guardados correctamente!");
                    // Opcional: Recargar para asegurar que se ve lo nuevo
                    // location.reload(); 
                } else {
                    alert("Error al guardar: " + (res.data.error || "Desconocido"));
                }
            } catch (error) {
                console.error(error);
                alert("Error de conexión.");
            }
        });
    }
});