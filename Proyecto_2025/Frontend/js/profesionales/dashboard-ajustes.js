//modificado y listo
import { apiGet, apiPut} from "../core/api.js";

document.addEventListener("DOMContentLoaded", () =>{
    console.log("dashboard-ajustes.js cargado.");

    const form = document.getElementById("form-ajustes");

    //Inputs

    const inputNombre = document.getElementById("nombre-negocio");
    const inputTelefono = document.getElementById("telefono-negocio");
    const inputDireccion = document.getElementById("direccion-negocio");

    //tomamos negocio id del usuario logueado
    const NEGOCIO_ID = localStorage.getItem("negocio_id"); 

    if (!NEGOCIO_ID) {
        console.error("No se encontró NEGOCIO_ID en localStorage.");
        alert("Error: No se pudo cargar el negocio.");
        return;
    }

    //Carga de datos iniciales (editado, datos mock borrados)

    async function cargarDatos() {
        console.log("Cargando datos del negocio...");

        const res = await apiGet(`/negocios/${NEGOCIO_ID}`);

        if (!res.ok || res.error) {
            console.error("Error cargando negocio:", res.error);
            alert("Error al cargar los datos del negocio.");
            return;
        }

        // Llenar inputs con datos reales
        inputNombre.value = res.nombre;
        inputTelefono.value = res.telefono;
        inputDireccion.value = res.direccion;

    }

    cargarDatos();

    //guardar cambios

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            nombre: inputNombre.value.trim(),
            telefono: inputTelefono.value.trim(),
            direccion: inputDireccion.value.trim()
        };

        console.log("Datos listos para enviar:",payload);

        const res = await apiPut(`/negocios/${NEGOCIO_ID}`, payload);
    
        if (!res.ok || res.error) {
            console.error("Error al guardar cambios:", res.error);
            alert("No se pudieron guardar los cambios.");
            return;
        }

        alert("Cambios guardados correctamente");
    });
});;


