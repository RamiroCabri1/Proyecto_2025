import { apiGet } from "../core/api.js";

document.addEventListener("DOMContentLoaded", async () => {
    console.log("sacar-turno.js cargado.");

    const selectNegocio = document.getElementById("negocio");
    const selectProfesional = document.getElementById("profesional");
    const selectServicio = document.getElementById("servicio");
    const inputFecha = document.getElementById("fecha");
    const gridHorarios = document.getElementById("horarios-grid");
    const form = document.querySelector("form");

    let allProfesionales = [];
    let allServicios = [];
    let horarioSeleccionado = null;

    // 1. Carga inicial de datos
    try {
        const [resNegocios, resProfesionales, resServicios] = await Promise.all([
            apiGet("/negocios", false),
            apiGet("/profesionales", false),
            apiGet("/servicios", false)
        ]);

        if (resNegocios.status === 200) {
            llenarSelect(selectNegocio, resNegocios.data, "Seleccionar negocio");
        }

        if (resProfesionales.status === 200) allProfesionales = resProfesionales.data;
        if (resServicios.status === 200) allServicios = resServicios.data;

    } catch (error) {
        console.error("Error cargando datos iniciales:", error);
    }

    // 2. Lógica de filtrado por Negocio
    selectNegocio.addEventListener("change", () => {
        const negocioId = parseInt(selectNegocio.value);
        
        selectProfesional.innerHTML = '<option value="">Seleccionar profesional</option>';
        selectServicio.innerHTML = '<option value="">Seleccionar servicio</option>';
        gridHorarios.innerHTML = '<p class="placeholder-horarios">Seleccioná un día para ver los horarios disponibles</p>';

        if (!negocioId) return;

        const profsFiltrados = allProfesionales.filter(p => p.negocio_id === negocioId && p.activo);
        const servsFiltrados = allServicios.filter(s => s.negocio_id === negocioId);

        llenarSelect(selectProfesional, profsFiltrados);
        llenarSelect(selectServicio, servsFiltrados);
    });

    // 3. Calculadora de Horarios
    const calcularHorarios = async () => {
        const profesionalId = selectProfesional.value;
        const servicioId = selectServicio.value;
        const fecha = inputFecha.value;

        if (!profesionalId || !servicioId || !fecha) return;

        gridHorarios.innerHTML = "Cargando disponibilidad...";

        try {
            const dateObj = new Date(fecha + "T00:00:00");
            let diaSemana = dateObj.getDay(); 
            if (diaSemana === 0) diaSemana = 7;

            const res = await apiGet(`/profesionales/${profesionalId}/disponibilidad`, false);
            
            if (res.status !== 200) {
                gridHorarios.innerHTML = "Error al consultar disponibilidad.";
                return;
            }

            const horarioDelDia = res.data.find(d => d.dia_semana === diaSemana);

            if (!horarioDelDia) {
                gridHorarios.innerHTML = "<p>El profesional no trabaja este día.</p>";
                return;
            }

            const servicioObj = allServicios.find(s => s.id == servicioId);
            const duracion = servicioObj ? servicioObj.duracion_turno_min : 60;

            generarBotonesHorarios(horarioDelDia.hora_inicio, horarioDelDia.hora_fin, duracion);

        } catch (error) {
            console.error(error);
            gridHorarios.innerHTML = "Error calculando horarios.";
        }
    };

    selectProfesional.addEventListener("change", calcularHorarios);
    selectServicio.addEventListener("change", calcularHorarios);
    inputFecha.addEventListener("change", calcularHorarios);


    // 4. Generador de botones visuales
    function generarBotonesHorarios(inicioStr, finStr, duracionMin) {
        gridHorarios.innerHTML = "";
        
        const aMinutos = (timeStr) => {
            const [h, m] = timeStr.split(":").map(Number);
            return h * 60 + m;
        };

        const aHora = (mins) => {
            const h = Math.floor(mins / 60).toString().padStart(2, '0');
            const m = (mins % 60).toString().padStart(2, '0');
            return `${h}:${m}`;
        };

        let actual = aMinutos(inicioStr);
        const fin = aMinutos(finStr);

        while (actual + duracionMin <= fin) {
            const horaTexto = aHora(actual);
            
            const btn = document.createElement("button");
            btn.type = "button"; 
            btn.className = "horario"; 
            btn.textContent = horaTexto;

            btn.onclick = () => {
                document.querySelectorAll(".horario").forEach(b => b.classList.remove("selected"));
                btn.classList.add("selected");
                horarioSeleccionado = horaTexto;
            };

            gridHorarios.appendChild(btn);
            actual += duracionMin;
        }

        if (gridHorarios.innerHTML === "") {
            gridHorarios.innerHTML = "<p>No hay turnos disponibles en este rango.</p>";
        }
    }

    // 5. Submit del formulario
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        if (!horarioSeleccionado) {
            alert("Por favor, seleccioná un horario.");
            return;
        }

        const fechaCompleta = `${inputFecha.value} ${horarioSeleccionado}:00`;

        const params = new URLSearchParams({
            negocio_id: selectNegocio.value,
            profesional_id: selectProfesional.value,
            servicio_id: selectServicio.value,
            horario: fechaCompleta
        });

        window.location.href = `clientes-ingresar-datos.html?${params.toString()}`;
    });

    function llenarSelect(select, datos, placeholder) {
        if(placeholder) select.innerHTML = `<option value="">${placeholder}</option>`;
        else select.innerHTML = "";

        datos.forEach(d => {
            const option = document.createElement("option");
            option.value = d.id;
            option.textContent = d.nombre;
            select.appendChild(option);
        });
    }
});