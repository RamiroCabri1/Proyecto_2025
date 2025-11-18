document.addEventListener("DOMContentLoaded", () =>{
    console.log("clientes-ingresar-datos.js cargado");

    const form = document.getElementById("form-datos-turno");

    //tomar datos (prueba)
    const params = new URLSearchParams(window.location.search);

    const profesionales_id = params.get("profesional_id");
    const servicio_id = params.get("servicio_id");
    const horario = params.get("horario");
    const negocio_id = params.get("negocio_id");

    //guardarlos en hidden inputs
    document.getElementById("profesional_id").value = profesionales_id;
    document.getElementById("servicio_id").value = servicio_id;
    document.getElementById("horario").value = horario;
    document.getElementsById("negocio_id").value = horario;

    form.addEventListener("submit", (e)=>{
        e.preventDefault();


        //DATOS DE CLIENTE
        const nombre = document.getElementById("nombre").value.trim();
        const apellido = document.getElementById("apellido").value.trim();
        const dni = document.getElementById("dni").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const email = document.getElementById("email").value.trim();

        //Creamos obj turno
        const turnoEnProceso = {
            profesionales_id,
            servicio_id,
            horario,
            negocio_id
        };

        //guardamos en localStorage
        localStorage.setItem("turnoEnProceso", JSON.stringify(turnoEnProceso));

        console.log("Turno cargado en memoria:", turnoEnProceso);

        //pag de confirmacion
        window.location.href = "./clientes-turno-detalle.html"
    })
})
