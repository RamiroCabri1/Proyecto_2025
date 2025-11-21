//revisado y listo

// URL del backend. Todas mis solicitudes salen de esta URL >:)

const API_URL = "http://localhost:5000";

//--------------------TOKEN------------------//

//Pedimos token guardado en navegador
function getToken(){
    return localStorage.getItem("token");
}

//---Request---------------//

export async function apiRequest(method, endpoint, data = null, useAuth = true) {

    const options = {
        method,
        headers: {}
    };

// Si enviamos datos agregar body JSON
if(data){
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(data);
}

//si solicitud requiere auth, aniadimos token
if(useAuth){
    const token = getToken();
    if (token){
        options.headers["Authorization"] = `Bearer ${token}`;
    }
}

try{
    const response = await fetch(API_URL + endpoint, options);

    //intentamos parsear JSON
    const json = await response.json().catch(() => ({}));

    return {
            ok: response.ok,
            status: response.status,
            ...json
        };

    } catch (error) {
        console.error("Error en la API:", error);

        return {
            ok: false,
            status: 500,
            error: "Error en la conexión con el servidor"
        };
    }
}

// Helpersss
export function apiGet(endpoint) {
    return apiRequest("GET", endpoint);
}

export function apiPost(endpoint, data, useAuth = true) {
    return apiRequest("POST", endpoint, data, useAuth);
}

export function apiPut(endpoint, data) {
    return apiRequest("PUT", endpoint, data);
}

export function apiDelete(endpoint) {
    return apiRequest("DELETE", endpoint);
}