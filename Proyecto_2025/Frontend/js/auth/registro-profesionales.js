//ya modificada y lista

import { apiPost } from "../core/api.js"

document.addEventListener("DOMContentLoaded", () => {
    console.log("registro-profesionales.js cargado");

    const form = document.getElementById("form-registro-profesional");

    form.addEventListener("submit", async (e) =>{
        e.preventDefault();

        const nombre = document.getElementById("nombre").value.trim();
        const email = document.getElementById("email").value.trim();
        const pass1 = document.getElementById("password").value.trim();
        const pass2 = document.getElementById("password2").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const direccion = document.getElementById("direccion").value.trim();


        //validacion de constraseñas
        if (pass1 !== pass2){
            alert("Las contraseñas no coiciden");
            return;
        }

        //crear cuenta negocio
        const payloadNegocio ={
            nombre: nombreNegocio,
            direccion,
            telefono
        };

        const resNegocio = await apiPost("/negocios", payloadNegocio);

        if (!resNegocio || resNegocio.error){
            alert("Error al crear negocio: " + (resNegocio?.error || "desconocido"));
            return;

        }

        const negocioId = resNegocio.id;
        console.log("Negocio creado:", resNegocio);


        //crear usuario duenio
        const payloadUsuario = {
            email, 
            password: pass1,
            negocio_id: negocioId
        };

        const resUsuario = await apiPost("/registro", payloadUsuario);

        if (!resUsuario || resUsuario.error){
            alert("Error al registrar usuario" + (resUsuario?.error || "desconocido"));
            return;
        }

        console.log("Usuario registrado:", resUsuario);





        // Flujo exitoso
        alert("Registro completdo")
        window.location.href = "./login-profesionales.html";
    });
});