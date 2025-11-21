//ya modificada para probar

import { apiPost } from "../core/api.js"

//Ni bien carga pag
document.addEventListener("DOMContentLoaded", () => {
    console.log("JS Login cargado correctamente.");

    const form = document.getElementById("form-login-profesionales");
    const errorMsg = document.getElementById("error-message");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        //tomar valores de formulario
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        //crear objeto para mandar a backend
        const data = {email, password};

        //Hacer POST al backend (ya modificado)
        const res = await apiPost("/login", data, false);

        console.log("Resultado login:", res)

        //backend devuelve token si todo salio bien
        if (res && res.token){ 
    
            // Guardar token
            localStorage.setItem("token", res.token);

            // Guardar negocio_id que viene desde el backend
            localStorage.setItem("negocio_id", res.negocio_id);

           // Redirigir
            window.location.href = "./dashboard-ajustes.html";
            return;
        }


        //Mostrar error si falla
        errorMsg.style.display = "block";
        errorMsg.textContent = "Usuario y/o contraseña incorrectos.";
        


    });
});