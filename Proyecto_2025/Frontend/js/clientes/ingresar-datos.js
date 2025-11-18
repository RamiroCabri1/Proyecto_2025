import { apiGet, apiPut } from "../core/api.js";

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

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        // datos del cliente
        const nombre = document.getElementById("nombre").value.trim();
        const apellido = document.getElementById("apellido").value.trim();
        const dni = document.getElementById("dni").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const email = document.getElementById("email").value.trim();

        // Datos mock para ejemplooooooo
        const profesionalesMock = {
            "101": "María Pérez",
            "102": "Carolina Díaz",
            "201": "Julieta Romero",
            "301": "Fabián Torres"
        };

        const serviciosMock = {
            "1": "Masajes",
            "2": "Color",
            "3": "Limpieza Facial",
            "4": "Depilación",
            "5": "Pestañas",
            "6": "Kinesiología Deportiva"
        };

        // OBJETO final del turno
        const turnoCompleto = {
            cliente_nombre: `${nombre} ${apellido}`,
            cliente_dni: dni,
            cliente_telefono: telefono,
            cliente_email: email,

            profesional_id,
            profesional_nombre: profesionalesMock[profesional_id] || "—",

            servicio_id,
            servicio_nombre: serviciosMock[servicio_id] || "—",

            fecha,
            horario,
            negocio_id,


            //esto es lo que les decia que convierte el ID en un codigo, es hermosoooo
            codigo: "TUR-" + Math.floor(100000 + Math.random() * 900000),
            estado: "Pendiente"
        };

        // Guardar turno final
        localStorage.setItem("turnoEnProceso", JSON.stringify(turnoCompleto));

        console.log("Turno guardado:", turnoCompleto);

        // Redirigir
        window.location.href = "./clientes-turno-detalle.html";
    });
});

