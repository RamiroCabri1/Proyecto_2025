import { apiGet, apiPut} from "../core/api.js";

document.addEventListener("DOMContentLoaded", () =>{
    console.log("dashboard-ajustes.js cargado.");

    const form = document.getElementById("form-ajustes");

    //Inputs

    const inputNombre = document.getElementById("nombre-negocio");
    const inputTelefono = document.getElementById("telefono-negocio");
    const inputDireccion = document.getElementById("direccion-negocio");
    const inputApertura = document.getElementById("hora-apertura");
    const inputCierre = document.getElementById("hora-cierre");


    const NEGOCIO_ID = localStorage.getItem("negocio_id")  || 1; 


    //Carga de datos iniciales

    async function cargarDatos() {
        console.log("Cargando datos del negocio . . . ")

    //Hardcodeado x ahora
        const datosFalsos = {
            nombre: "nombre del negociooo",
            telefono: "29114444444",
            direccion: "cashe 123",
            hora_apertura: "09:00",
            hora_cierre: "10:00"
        };

        //rellenar inputs
        inputNombre.value = datosFalsos.nombre;
        inputTelefono.value = datosFalsos.telefono;
        inputDireccion.value = datosFalsos.direccion;
        inputApertura.value = datosFalsos.apertura;
        inputCierre.value = datosFalsos.cierre;

    }


    cargarDatos();

    //guardar cambios

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            nombre: inputNombre.value.trim(),
            telefono: inputTelefono.value.trim(),
            direccion: inputDireccion.value.trim(),
            hora_apertura: inputApertura.value,
            hora_cierre: inputCierre.value
        };

        console.log("Datos listos pra enviar:",payload);

        alert("Cambios guardados");
    });
});



//FALTA BACKEND ESTO ES UNA SIMULACIONNNNNNNNNNNNN