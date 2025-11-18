console.log("consultar-turno.js cargado.");

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("form-consulta-turno");
    const inputCodigo = document.getElementById("codigo");
    const mensajeError = document.getElementById("mensaje-error");

    // Turnos de mentiritas a cambiar
    const turnosMock = [
        { codigo: "TUR-000123", nombre: "Ana Lopez", profesional: "Maria Perez", servicio: "Color", fecha: "2025-02-15", horario: "10:00" },
        { codigo: "TUR-000456", nombre: "Carlos Diaz", profesional: "Carolina Diaz", servicio: "Masajes", fecha: "2025-02-18", horario: "15:30" },
        { codigo: "TUR-000789", nombre: "Laura Gomez", profesional: "Julieta Romero", servicio: "Depilación", fecha: "2025-02-22", horario: "09:30" }
    ];

    // Submit
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const codigoIngresado = inputCodigo.value.trim().toUpperCase();

        mensajeError.textContent = "";
        mensajeError.style.display = "none";

        // Validacion
        const regex = /^TUR-\d{6}$/;
        if (!regex.test(codigoIngresado)) {
            mensajeError.textContent = "El formato del código no es válido (Ej: TUR-000123).";
            mensajeError.style.display = "block";
            return;
        }

        // Buscar turno en mock
        const turno = turnosMock.find(t => t.codigo === codigoIngresado);

        if (!turno) {
            mensajeError.textContent = "No se encontró ningún turno con ese código.";
            mensajeError.style.display = "block";
            return;
        }

        // Aca guardamos el turno encontrado para mostrarlo en la página de detalle
        localStorage.setItem("turnoConsultado", JSON.stringify(turno));

        // Redirigir al detalle
        window.location.href = `clientes-turno-detalle.html?codigo=${codigoIngresado}`;
    });

});
