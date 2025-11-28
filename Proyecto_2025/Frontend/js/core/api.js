// URL del backend. Todas mis solicitudes salen de esta URL >:)

const API_URL = "http://localhost:5000";




 function getToken(){

    return localStorage.getItem("token");
}

//---Request Genérica---------------//
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

    // Si solicitud requiere auth, envia token
    if(useAuth){
        const token = getToken();
        if (token){
            options.headers["x-access-token"] = token;
        }
    }

    try{
        const response = await fetch(API_URL + endpoint, options);

        let responseData = {};
        try{
            responseData = await response.json();
        } catch{}

        return { status: response.status, data: responseData };

    } catch (error) {
        console.error("Error en la API:", error);
        return { status: 500, data:{ error: "Error de conexión" } };
    }
}

export function apiGet(endpoint, useAuth = true){
    return apiRequest("GET", endpoint, null, useAuth);
}

export function apiPost(endpoint, data, useAuth = true){
    return apiRequest("POST", endpoint, data, useAuth);
}

export function apiPut(endpoint, data, useAuth = true){
    return apiRequest("PUT", endpoint, data, useAuth);
}

export function apiDelete(endpoint, useAuth = true){
    return apiRequest("DELETE", endpoint, null, useAuth);
}