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

        //Hacer POST al backend
        const res = await apiPost("/profesionales/login", data, false);

        console.log("Resultado login:", res)

        //backend devuelve 200 -> OK
        if (res.status === 200 && res.data.token){
            
            //guardar token en localstorage
            localStorage.setItem("token",res.data.token);

            //guardar ID del negocio o prof. si el backend lo envia
            if (res.data.negocio_id){
                localStorage.setItem("negocio_id", res.data.negocio_id)
            }

            //redirigir a dashboard
            window.location.href = "./dahsboard-clientes.html";
            return;
        }

        //Mostrar error si falla
        errorMsg.style.display = "block";
        errorMsg.textContent = "Usuario y/o contraseña incorrectos.";
        


    });
});