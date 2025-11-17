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


        //validaciones
        if (pass1 !== pass2){
            alert("Las contraseñas no coiciden");
            return;
        }

        const payload ={
            nombre,
            email,
            password: pass1,
            telefono,
            direccion
        };

        console.log("Registrando profesional:", payload);

        alert("Registro completdo")
        window.location.href = "./login-profesionales.html";
    });
});