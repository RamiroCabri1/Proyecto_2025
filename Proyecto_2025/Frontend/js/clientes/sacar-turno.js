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

    // 1. Carga inicial
    try {
        const [resNegocios, resProfesionales, resServicios] = await Promise.all([
            apiGet("/negocios", false),
            apiGet("/profesionales", false),
            apiGet("/servicios", false)
        ]);

        if (resNegocios.status === 200) llenarSelect(selectNegocio, resNegocios.data, "Seleccionar negocio");
        if (resProfesionales.status === 200) allProfesionales = resProfesionales.data;
        if (resServicios.status === 200) allServicios = resServicios.data;

    } catch (error) { console.error(error); }

    // 2. Filtrado por Negocio
    selectNegocio.addEventListener("change", () => {
        const negocioId = parseInt(selectNegocio.value);
        
        selectProfesional.innerHTML = '<option value="">Seleccionar profesional</option>';
        selectServicio.innerHTML = '<option value="">Seleccionar servicio</option>';
        gridHorarios.innerHTML = '<p class="placeholder-horarios">Seleccioná un día...</p>';

        if (!negocioId) return;

        const profsFiltrados = allProfesionales.filter(p => p.negocio_id === negocioId && p.activo);
        const servsFiltrados = allServicios.filter(s => s.negocio_id === negocioId);

        llenarSelect(selectProfesional, profsFiltrados);
        llenarSelect(selectServicio, servsFiltrados);
    });

    // 3. Calcular Horarios
    const calcularHorarios = async () => {
        const [profId, servId, fecha] = [selectProfesional.value, selectServicio.value, inputFecha.value];
        if (!profId || !servId || !fecha) return;

        gridHorarios.innerHTML = "Cargando...";

        try {
            const dateObj = new Date(fecha + "T00:00:00");
            let diaSemana = dateObj.getDay(); 
            if (diaSemana === 0) diaSemana = 7;

            const res = await apiGet(`/profesionales/${profId}/disponibilidad`, false);
            
            if (res.status !== 200) { gridHorarios.innerHTML = "Error disponibilidad."; return; }

            const horarioDelDia = res.data.find(d => d.dia_semana === diaSemana);

            if (!horarioDelDia) {
                gridHorarios.innerHTML = "<p>El profesional no trabaja este día.</p>";
                return;
            }

            const servicioObj = allServicios.find(s => s.id == servId);
            const duracion = servicioObj ? servicioObj.duracion_turno_min : 60;

            generarBotones(horarioDelDia.hora_inicio, horarioDelDia.hora_fin, duracion);

        } catch (error) { gridHorarios.innerHTML = "Error."; }
    };

    [selectProfesional, selectServicio, inputFecha].forEach(el => el.addEventListener("change", calcularHorarios));

    // 4. Generar Botones
    function generarBotones(inicioStr, finStr, duracionMin) {
        gridHorarios.innerHTML = "";
        
        const aMinutos = (s) => { const [h, m] = s.split(":").map(Number); return h * 60 + m; };
        const aHora = (min) => {
            const h = Math.floor(min / 60).toString().padStart(2, '0');
            const m = (min % 60).toString().padStart(2, '0');
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
        if (gridHorarios.innerHTML === "") gridHorarios.innerHTML = "<p>Sin turnos disponibles.</p>";
    }

    // 5. Submit
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        if (!horarioSeleccionado) return alert("Seleccioná un horario.");

        const params = new URLSearchParams({
            negocio_id: selectNegocio.value,
            profesional_id: selectProfesional.value,
            servicio_id: selectServicio.value,
            horario: `${inputFecha.value} ${horarioSeleccionado}:00`
        });

        window.location.href = `clientes-ingresar-datos.html?${params.toString()}`;
    });

    function llenarSelect(sel, datos, placeholder) {
        sel.innerHTML = placeholder ? `<option value="">${placeholder}</option>` : "";
        datos.forEach(d => {
            const opt = document.createElement("option");
            opt.value = d.id;
            opt.textContent = d.nombre;
            sel.appendChild(opt);
        });
    }
});