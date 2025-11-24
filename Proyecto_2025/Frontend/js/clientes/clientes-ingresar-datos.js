import { apiGet, apiPost } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("clientes-ingresar-datos.js cargado (Versión Fusionada)");

    const form = document.getElementById("form-datos-turno");

    // Leer datos de la URL
    const params = new URLSearchParams(window.location.search);
    const profesional_id = params.get("profesional_id");
    const servicio_id = params.get("servicio_id");
    const horario = params.get("horario"); // "YYYY-MM-DD HH:MM:SS"
    const negocio_id = params.get("negocio_id");

    // Llenar inputs ocultos si existen en el HTML
    const inputProf = document.getElementById("profesional_id");
    if(inputProf) inputProf.value = profesional_id;
    
    // Lógica Visual: Cargar el Resumen
    async function cargarResumen() {
        try {
            const [profRes, servRes] = await Promise.all([
                apiGet(`/profesionales/${profesional_id}`, false),
                apiGet(`/servicios/${servicio_id}`, false)
            ]);

            const nombreProf = (profRes.status === 200) ? profRes.data.nombre : "Profesional";
            const nombreServ = (servRes.status === 200) ? servRes.data.nombre : "Servicio";

            // Formateo de fecha para que se vea lindo
            const [fechaPart, horaPart] = horario.split(" ");
            const horaCorta = horaPart.substring(0, 5);

            const resumen = document.getElementById("resumen-turno");
            
            const contenedorResumen = resumen || document.querySelector(".resumen-turno");

            if (contenedorResumen) {
                contenedorResumen.innerHTML = `
                    Estás reservando con <strong>${nombreProf}</strong> para 
                    <strong>${nombreServ}</strong> el día 
                    <strong>${fechaPart} a las ${horaCorta}</strong>.
                `;
            }
        } catch (error) {
            console.error("Error cargando resumen visual:", error);
        }
    }

    // Ejecutamos la carga visual
    cargarResumen();


    //  Lógica Funcional
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Captura de datos
        const nombre = document.getElementById("nombre").value.trim();
        const apellido = document.getElementById("apellido").value.trim();
        const dni = document.getElementById("dni").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const email = document.getElementById("email").value.trim();

        const nuevoCliente = {
            nombre, apellido, dni, telefono, email,
            negocio_id: parseInt(negocio_id)
        };

        try {
            // A. Crear Cliente (POST)
            console.log("Creando cliente...");
            const resCliente = await apiPost("/clientes", nuevoCliente, false);

            let clienteIdFinal = null;

            if (resCliente.status === 201) {
                clienteIdFinal = resCliente.data.id;
            } else if (resCliente.status === 409) {
                alert("Ese DNI ya está registrado. Por favor, usá otro o contactá al negocio.");
                return; 
            } else {
                alert("Error creando cliente: " + (resCliente.data.error || "Desconocido"));
                return;
            }

            // B. Crear Turno (POST)
            if (clienteIdFinal) {
                const nuevoTurno = {
                    fecha_hora: horario,
                    cliente_id: clienteIdFinal,
                    profesional_id: parseInt(profesional_id),
                    servicio_id: parseInt(servicio_id),
                    negocio_id: parseInt(negocio_id)
                };

                const resTurno = await apiPost("/turnos", nuevoTurno, false);

                if (resTurno.status === 201) {
                    localStorage.setItem("turnoCreadoId", resTurno.data.id);
                    window.location.href = "./clientes-turno-detalle.html";
                } else {
                    alert("Error creando turno: " + (resTurno.data.error || "Ocupado"));
                }
            }

        } catch (error) {
            console.error(error);
            alert("Error de conexión");
        }
    });
});