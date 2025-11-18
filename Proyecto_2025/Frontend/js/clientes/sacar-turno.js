import { apiGet } from "../core/api.js"

document.addEventListener("DOMContentLoaded", () => {
    console.log("sacar-turno.js cargado.");

    const selectNegocio = document.getElementById("negocio");
    const selectProfesional = document.getElementById("profesional");
    const selectServicio = document.getElementById("servicio");
    const inputFecha = document.getElementById("fecha");
    const gridHorarios = document.getElementById("horarios-grid");
    const form = document.querySelector("form");

    // mockssssssss
    const profesionalesMock = {
        "1": [
            { id: 101, nombre: "Maria Sosa" },
            { id: 102, nombre: "Carolina Rossi" }
        ],
        "2": [
            { id: 201, nombre: "Julieta Romero" }
        ],
        "3": [
            { id: 301, nombre: "Fabian Torres" }
        ]
    };

    const serviciosMock = {
        "101": [
            { id: 1, nombre: "Masajes" },
            { id: 2, nombre: "Color" }
        ],
        "102": [
            { id: 3, nombre: "Limpieza Facial" }
        ],
        "201": [
            { id: 4, nombre: "Depilación" },
            { id: 5, nombre: "Pestañas" }
        ],
        "301": [
            { id: 6, nombre: "Kinesiología Deportiva" }
        ]
    };

    function obtenerHorariosMock() {
        return [
            "09:00", "09:30", "10:00",
            "10:30", "11:00", "11:30",
            "12:00", "12:30"
        ];
    }

    // Carga de prof. x negocio
    selectNegocio.addEventListener("change", () => {
        const idNegocio = selectNegocio.value;

        selectProfesional.innerHTML = `<option value="">Seleccionar profesional</option>`;
        selectServicio.innerHTML = `<option value="">Seleccionar servicio</option>`;
        gridHorarios.innerHTML = `<p class="placeholder-horarios">Seleccioná una fecha</p>`;

        if (!idNegocio) return;

        (profesionalesMock[idNegocio] || []).forEach(p => {
            const op = document.createElement("option");
            op.value = p.id;
            op.textContent = p.nombre;
            selectProfesional.appendChild(op);
        });
    });

    // Carga de servicios x profesional
    selectProfesional.addEventListener("change", () => {
        const profesionalID = selectProfesional.value;
        selectServicio.innerHTML = `<option value="">Seleccionar servicio</option>`;
        gridHorarios.innerHTML = `<p class="placeholder-horarios">Seleccioná una fecha</p>`;

        if (!profesionalID) return;

        (serviciosMock[profesionalID] || []).forEach(s => {
            const op = document.createElement("option");
            op.value = s.id;
            op.textContent = s.nombre;
            selectServicio.appendChild(op);
        });
    });

    // carga de horarios x fecha
    inputFecha.addEventListener("change", () => {
        const fecha = inputFecha.value;
        gridHorarios.innerHTML = "";

        if (!fecha) return;

        obtenerHorariosMock().forEach(hora => {
            const div = document.createElement("div");
            div.classList.add("horario");
            div.textContent = hora;

            div.addEventListener("click", () => {
                document.querySelectorAll(".horario").forEach(h => h.classList.remove("selected"));
                div.classList.add("selected");
            });

            gridHorarios.appendChild(div);
        });
    });

    // Boton sig. 
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const negocioID = selectNegocio.value;
        const profesionalID = selectProfesional.value;
        const servicioID = selectServicio.value;
        const fecha = inputFecha.value;
        const horario = document.querySelector(".horario.selected")?.textContent;

        if (!negocioID || !profesionalID || !servicioID || !fecha || !horario) {
            alert("Por favor complete todos los campos y seleccione un horario.");
            return;
        }

        const url = `clientes-ingresar-datos.html?negocio_id=${negocioID}&profesional_id=${profesionalID}&servicio_id=${servicioID}&horario=${horario}&fecha=${fecha}`;

        window.location.href = url;
    });

});
