import { apiGet, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", async () => {
    console.log("detalle-turno.js cargado.");

    const turnoId = localStorage.getItem("turnoCreadoId");

    if (!turnoId) {
        alert("No hay información del turno. Volviendo al inicio.");
        window.location.href = "clientes-turno.html";
        return;
    }

    console.log("Mostrando turno ID:", turnoId);

    // Pedimos los datos frescos a la BD
    try {
        const res = await apiGet(`/turnos/${turnoId}`, false);

        if (res.status === 200) {
            const turno = res.data;
            renderizarDetalle(turno);
        } else {
            console.error("Error:", res);
            document.querySelector("main").innerHTML = "<h2 style='text-align:center; color:red;'>Error: El turno ya no existe o fue borrado.</h2>";
            localStorage.removeItem("turnoCreadoId");
        }
    } catch (error) {
        console.error(error);
        alert("Error de conexión.");
    }

    // Función para llenar los huecos del HTML
    async function renderizarDetalle(turno) {
        setText("codigo-turno", "TUR-" + turno.id);

        if(turno.fecha_hora) {
            const [fecha, hora] = turno.fecha_hora.split(" ");
            setText("turno-fecha", fecha);
            setText("turno-horario", hora.substring(0, 5));
        }

        const estadoEl = document.getElementById("estado-turno");
        if(estadoEl) {
            estadoEl.textContent = turno.estado;
            estadoEl.style.color = (turno.estado === "Cancelado") ? "red" : "green";
        }

        // Buscar nombres reales
        setText("cliente-nombre", "Cargando...");
        setText("profesional-nombre", "Cargando...");
        setText("servicio-nombre", "Cargando...");

        try {
            const [resCliente, resProf, resServ] = await Promise.all([
                apiGet(`/clientes/${turno.cliente_id}`, false),
                apiGet(`/profesionales/${turno.profesional_id}`, false),
                apiGet(`/servicios/${turno.servicio_id}`, false)
            ]);

            if (resCliente.status === 200) setText("cliente-nombre", `${resCliente.data.nombre} ${resCliente.data.apellido || ''}`);
            if (resProf.status === 200) setText("profesional-nombre", resProf.data.nombre);
            if (resServ.status === 200) setText("servicio-nombre", resServ.data.nombre);

        } catch (error) {
            console.error("Error buscando nombres:", error);
        }

        // Ocultar botón cancelar si ya está cancelado
        if (turno.estado === "Cancelado") {
            const btn = document.querySelector(".btn.cancelar");
            if(btn) btn.style.display = "none";
        }
    }

    function setText(id, texto) {
        const el = document.getElementById(id);
        if (el) el.textContent = texto;
    }

    // Botón Cancelar
    const btnCancelar = document.querySelector(".btn.cancelar");
    if (btnCancelar) {
        btnCancelar.addEventListener("click", async (e) => {
            e.preventDefault();
            if (confirm("¿Estás seguro de que querés cancelar este turno?")) {
                const res = await apiDelete(`/turnos/${turnoId}`);
                if (res.status === 200) {
                    alert("Turno cancelado.");
                    window.location.reload();
                } else {
                    alert("Error al cancelar.");
                }
            }
        });
    }
    
    // Botón Volver
    const btnVolver = document.querySelector(".btn.volver");
    if(btnVolver) {
        btnVolver.addEventListener("click", () => {
        });
    }
});