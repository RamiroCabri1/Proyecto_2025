import { apiPost } from "../core/api.js";

document.addEventListener("DOMContentLoaded", () => {
    console.log("registro-profesionales.js cargado");

    const form = document.getElementById("form-registro-profesional");

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            // 1. Capturar todos los datos
            const nombreNegocio = document.getElementById("nombre").value.trim();
            const email = document.getElementById("email").value.trim();
            const pass1 = document.getElementById("password").value.trim();
            const pass2 = document.getElementById("password2").value.trim();
            const telefono = document.getElementById("telefono").value.trim();
            const direccion = document.getElementById("direccion").value.trim();

            // Validaciones básicas
            if (pass1 !== pass2) {
                alert("Las contraseñas no coinciden.");
                return;
            }
            if (pass1.length < 6) {
                alert("La contraseña debe tener al menos 6 caracteres.");
                return;
            }

            try {
                // --- PASO 1: CREAR EL NEGOCIO ---
                console.log("Creando negocio...");
                
                const negocioData = {
                    nombre: nombreNegocio,
                    direccion: direccion,
                    telefono: telefono
                };

                // false = sin token (es público)
                const resNegocio = await apiPost("/negocios", negocioData, false);

                if (resNegocio.status !== 201) {
                    alert("Error al crear el negocio: " + (resNegocio.data.error || "Desconocido"));
                    return;
                }

                const nuevoNegocioId = resNegocio.data.id;
                console.log("Negocio creado ID:", nuevoNegocioId);

                // --- PASO 2: CREAR EL USUARIO (ADMIN) ---
                console.log("Creando usuario administrador...");

                const usuarioData = {
                    email: email,
                    password: pass1,
                    negocio_id: nuevoNegocioId // ¡Acá vinculamos todo!
                };

                const resUsuario = await apiPost("/registro", usuarioData, false);

                if (resUsuario.status === 201) {
                    alert("¡Registro completado con éxito! Ahora iniciá sesión.");
                    window.location.href = "./login-profesionales.html";
                } else if (resUsuario.status === 409) {
                    alert("Ese email ya está registrado.");
                } else {
                    alert("Error al crear usuario: " + (resUsuario.data.error || "Desconocido"));
                }

            } catch (error) {
                console.error(error);
                alert("Error de conexión. Verificá que el servidor esté corriendo.");
            }
        });
    }
});