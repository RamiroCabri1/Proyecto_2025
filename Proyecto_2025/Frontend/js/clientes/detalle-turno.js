document.addEventListener("DOMContentLoaded", () => {
    console.log("turno-detalle.js cargado.");

    // Obtener turno guardado
    const turno = JSON.parse(localStorage.getItem("turnoEnProceso"));

    if (!turno) {
        alert("No se encontró información del turno.");
        window.location.href = "./clientes-turno.html";
        return;
    }

    // Mostrar codigooo
    document.getElementById("codigo-turno").textContent = turno.codigo;

    // Mostrar datos
    document.getElementById("cliente-nombre").textContent = turno.cliente_nombre;
    document.getElementById("profesional-nombre").textContent = turno.profesional_nombre;
    document.getElementById("servicio-nombre").textContent = turno.servicio_nombre;
    document.getElementById("turno-fecha").textContent = turno.fecha;
    document.getElementById("turno-horario").textContent = turno.horario;

    // Estado (MOCK de mentira)
    document.getElementById("estado-turno").textContent = turno.estado;

    // Cancelar turno (mock)
    const btnCancelar = document.querySelector(".btn.cancelar");

    btnCancelar.addEventListener("click", () => {
        const confirmacion = confirm("¿Seguro que querés cancelar el turno?");

        if (!confirmacion) return;

        // Simulación de cancelación
        turno.estado = "Cancelado";
        localStorage.setItem("turnoEnProceso", JSON.stringify(turno));

        document.getElementById("estado-turno").textContent = "Cancelado";

        alert("Tu turno fue cancelado.");
    });

});
