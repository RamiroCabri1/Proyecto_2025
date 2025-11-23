import { apiGet } from "../core/api.js"

document.addEventListener("DOMContentLoaded", () => {
    console.log("sacar-turno.js cargado.");

    const selectNegocio = document.getElementById("negocio");
    const selectProfesional = document.getElementById("profesional");
    const selectServicio = document.getElementById("servicio");
    const inputFecha = document.getElementById("fecha");
    const gridHorarios = document.getElementById("horarios-grid");
    const form = document.querySelector("form");

    // parte corregida y modificada

    let profesionales = [];
    let servicios = [];

    const DIAS_SEMANA = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];

    function obtenerDiaSemana(fechaStr) {
        if (!fechaStr) return null;
        //hora forzada p evitar lios de timezone
        const date = new Date(fechaStr + "T00:00:00");
        const idx = date.getDay();
        return DIAS_SEMANA[idx];
    }

    function generarHorarios(horaInicio, horaFin, duracionMin){
        const horarios = [];
        if (!horaInicio || !horaFin || !duracionMin) return horarios;

        const [hIni, mIni] = horaInicio.split(":").map(Number);
        const [hFin, mFin] = horaFin.split(":").map(Number);

        let inicio = hIni * 60 + mIni;
        const fin = hFin * 60 + mFin;

        while (inicio + duracionMin <= fin) {
            const h = Math.floor(inicio / 60);
            const m = inicio % 60;
            horarios.push(`${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`);
            inicio += duracionMin;
        }

        return horarios;
    }

    // Cargar negocios reales
    async function cargarNegocios() {
        try {
            const res = await apiGet("/negocios");

            if (!res.ok || res.error) {
                console.error("Error cargando negocios:", res.error);
                return;
            }

            // Asumimos que el backend devuelve un array de negocios
            const lista = Array.isArray(res) ? res : (res.data || []);

            selectNegocio.innerHTML = `<option value="">Seleccionar negocio</option>`;

            lista.forEach(neg => {
                const op = document.createElement("option");
                op.value = neg.id;
                op.textContent = neg.nombre;
                selectNegocio.appendChild(op);
            });

        } catch (err) {
            console.error("Error inesperado cargando negocios:", err);
        }
    }

    // Carga de prof. y serv. x negocio
    async function cargarProfesionalesYServicios(idNegocio) {
        //reset de selets y horarios

        selectProfesional.innerHTML = `<option value="">Seleccionar profesional</option>`;
        selectServicio.innerHTML = `<option value="">Seleccionar servicio</option>`;
        gridHorarios.innerHTML = `<p class="placeholder-horarios">Seleccioná una fecha</p>`;

        profesionales = [];
        servicios = [];

        if (!idNegocio) return;

        try {
            const [resProf, resServ] = await Promise.all([
                apiGet("/profesionales"),
                apiGet("/servicios")
            ]);

            // Profesionales
            if (!resProf.ok || resProf.error) {
                console.error("Error cargando profesionales:", resProf.error);
            } else {
                const listaProf = Array.isArray(resProf) ? resProf : (resProf.data || []);
                profesionales = listaProf.filter(p => p.negocio_id == idNegocio);

                profesionales.forEach(p => {
                    const op = document.createElement("option");
                    op.value = p.id;
                    op.textContent = p.nombre;
                    selectProfesional.appendChild(op);
                });
            }

            // Servicios
            if (!resServ.ok || resServ.error) {
                console.error("Error cargando servicios:", resServ.error);
            } else {
                const listaServ = Array.isArray(resServ) ? resServ : (resServ.data || []);
                servicios = listaServ.filter(s => s.negocio_id == idNegocio);

                servicios.forEach(s => {
                    const op = document.createElement("option");
                    op.value = s.id;
                    op.textContent = s.nombre;
                    selectServicio.appendChild(op);
                });
            }

        } catch (err) {
            console.error("Error inesperado cargando profesionales/servicios:", err);
        }
    }

    // carga de horarios segun profesionaeles x servicio x fecha
    async function cargarHorarios() {
        const profesionalID = selectProfesional.value;
        const servicioID = selectServicio.value;
        const fecha = inputFecha.value;

        gridHorarios.innerHTML = "";


        if (!profesionalID || !servicioID || !fecha) {
        gridHorarios.innerHTML = `<p class="placeholder-horarios">Seleccioná un día para ver los horarios disponibles</p>`;
            return;
        }

        const diaSemana = obtenerDiaSemana(fecha);
        if (!diaSemana) {
            gridHorarios.innerHTML = `<p class="placeholder-horarios">Fecha inválida.</p>`;
            return;
        }

        const servicio = servicios.find(s => String(s.id) === String(servicioID));
        if (!servicio) {
            gridHorarios.innerHTML = `<p class="placeholder-horarios">No se encontró la duración del servicio.</p>`;
            return;
        }

        try {
            const resDisp = await apiGet(`/disponibilidades?profesional_id=${profesionalID}`);

            if (!resDisp.ok || resDisp.error) {
                console.error("Error obteniendo disponibilidades:", resDisp.error);
                gridHorarios.innerHTML = `<p class="placeholder-horarios">No fue posible obtener los horarios.</p>`;
                return;
            }

            const listaDisp = Array.isArray(resDisp.data) ? resDisp.data : [];
            const dispDia = listaDisp.find(d => d.dia_semana?.toLowerCase() === diaSemana);

            if (!dispDia) {
                gridHorarios.innerHTML = `<p class="placeholder-horarios">Este profesional no tiene horarios disponibles ese día.</p>`;
                return;
            }

            const horarios = generarHorarios(
                dispDia.hora_inicio,
                dispDia.hora_fin,
                servicio.duracion_turno_min
            );

            if (!horarios.length) {
                gridHorarios.innerHTML = `<p class="placeholder-horarios">No hay horarios disponibles para ese día.</p>`;
                return;
            }

            horarios.forEach(hora => {
                const div = document.createElement("div");
                div.classList.add("horario");
                div.textContent = hora;

                div.addEventListener("click", () => {
                    document.querySelectorAll(".horario").forEach(h => h.classList.remove("selected"));
                    div.classList.add("selected");
                });

                gridHorarios.appendChild(div);
            });

        } catch (err) {
            console.error("Error inesperado cargando horarios:", err);
            gridHorarios.innerHTML = `<p class="placeholder-horarios">Ocurrió un error al obtener los horarios.</p>`;
        }
    }

    // Eventos

    // Cambio de negocio/recargar profesionales y servicios
    selectNegocio.addEventListener("change", () => {
        const idNegocio = selectNegocio.value;
        cargarProfesionalesYServicios(idNegocio);
    });

    // Si cambia profesional o servicio y ya hay fecha, recalculamos horarios
    selectProfesional.addEventListener("change", () => {
        if (inputFecha.value) {
            cargarHorarios();
        } else {
            gridHorarios.innerHTML = `<p class="placeholder-horarios">Seleccioná una fecha para ver los horarios disponibles</p>`;
        }
    });

    selectServicio.addEventListener("change", () => {
        if (inputFecha.value) {
            cargarHorarios();
        } else {
            gridHorarios.innerHTML = `<p class="placeholder-horarios">Seleccioná una fecha para ver los horarios disponibles</p>`;
        }
    });

    // Cambio de fecha/ recalcular horarios
    inputFecha.addEventListener("change", () => {
        cargarHorarios();
    });

    // Boton siguiente
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

    cargarNegocios();
});