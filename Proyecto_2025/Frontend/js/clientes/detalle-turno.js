import { apiGet, apiDelete } from "../core/api.js";

document.addEventListener("DOMContentLoaded", async () => {
    console.log("detalle-turno.js cargado.");

    // 1. Recuperamos el ID del turno
    const turnoId = localStorage.getItem("turnoCreadoId");

    if (!turnoId) {
        alert("No hay turno seleccionado. Volviendo al inicio.");
        window.location.href = "clientes-turno.html";
        return;
    }

    console.log("Cargando Turno ID:", turnoId);

    // 2. Pedimos los datos frescos al Backend
    try {
        const res = await apiGet(`/turnos/${turnoId}`, false);

        if (res.status === 200) {
            const turno = res.data;
            await renderizarDetalle(turno);
        } else {
            console.error("Error:", res);
            document.querySelector("main").innerHTML = "<h2 style='text-align:center; color:red; margin-top: 2rem;'>No se encontró el turno solicitado.</h2>";
        }
    } catch (error) {
        console.error(error);
        alert("Error de conexión al cargar el turno.");
    }

    // 3. Función para llenar los huecos
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
            estadoEl.style.color = (turno.estado === "Cancelado") ? "#d9534f" : "#5cb85c";
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
        
        // Si está cancelado, escondemos el botón de cancelar
        if (turno.estado === "Cancelado") {
            const btn = document.querySelector(".btn.cancelar");
            if(btn) btn.style.display = "none";
        }
    }

    function setText(id, texto) {
        const el = document.getElementById(id);
        if (el) el.textContent = texto;
    }

    // 4. Botón Cancelar
    const btnCancelar = document.querySelector(".btn.cancelar");
    if (btnCancelar) {
        btnCancelar.addEventListener("click", async (e) => {
            e.preventDefault();
            if (confirm("¿Estás seguro de que querés cancelar este turno?")) {
                try {
                    const res = await apiDelete(`/turnos/${turnoId}`);
                    if (res.status === 200) {
                        alert("Turno cancelado correctamente.");
                        window.location.reload(); // Recargar para ver el estado nuevo
                    } else {
                        alert("Error al cancelar: " + (res.data.error || "Desconocido"));
                    }
                } catch (error) {
                    console.error(error);
                }
            }
        });
    }
});