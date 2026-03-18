# 📡 Guía de Consumo de la API - Generador de QR

Este documento explica de forma detallada cómo funciona el endpoint de generación de Códigos QR, cómo consumirlo fácilmente desde otras aplicaciones web o móviles (front-ends), y cómo desplegar la API gratuitamente en internet.

---

## 🚀 1. Despliegue en la Nube (Hosting Gratuito)

Para que tu API sea accesible de forma global, se recomienda utilizar el servicio gratuito de **Render.com**.

### Pasos para desplegar en Render:
1. Asegúrate de tener tu código subido en un repositorio de **GitHub**. *(Gracias a esto, Render automáticamente reconstruirá la app cada vez que hagas push).*
2. Entra a [Render](https://render.com/) e inicia sesión vinculando tu cuenta con GitHub.
3. Haz clic en **"New"** > **"Web Service"**.
4. Selecciona el repositorio donde subiste el proyecto.
5. Configura el servicio de la siguiente forma:
   - **Environment / Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Plan Free (Gratuito / $0 mes).
6. Haz clic en crear y espera un par de minutos que instalen las dependencias en la nube. Te dará una URL pública tipo `https://tu-generador-qr.onrender.com`.

> **Nota para planes gratis**: Los servicios gratuitos de Render suelen "hibernar" (dormirse) si llevan más de 15 minutos sin ser usados. La primera vez que alguien consuma la API al despertar tardará de 30 a 50 segundos en responder. Todos los usuarios posteriores recibirán su QR en milisegundos. 

---

## 🛠 2. Consumo del Endpoint Principal

El servicio principal es una ruta o endpoint tipo **GET** y se caracteriza por retornar directamente el archivo multimedia final (imagen `PNG`), en lugar de retornar un texto JSON complejo en base64. 

Esta técnica de retorno es ideal para inyectar los códigos rápidamente en etiquetas de imágenes para la web, apps en iOS/Android o documentos PDF (Facturas).

### Especificación del Endpoint:
```http
GET /generar-qr
```

### Parámetros de la URL (Query Params):

| Parámetro    | Obligatorio | Valor por defecto | Descripción                                                                                   |
| :---         | :---:       | :---              | :---                                                                                          |
| `texto`      | **SÍ**      | -                 | La información (un código UUID de base de datos, URL, token) que codificará el QR. Ej: `https://...` |
| `fill_color` | No          | `black`           | El color de la grilla interna del QR. Puede ser un nombre HTML o hexadecimal. Ej: `red` o `#FF0000` |
| `back_color` | No          | `white`           | El color del manto en el fondo del QR. Ej: `white`, `#FFFFFF` o `transparent` para interfaces oscuras |

---

## 💻 3. Ejemplos Rápidos de Implementación

Dado el formato de respuesta del endpoint de nuestra API, no es necesario hacer peticiones complejas con *Axios* o *Fetch* programáticamente. Simplemente apuntamos el origen multimedia al servidor con sus respectivas variables en la URL (`Query`):

**(Simularems que ya hemos subido el código a `https://api-qr.onrender.com`)**

### 🌐 Ejemplo en HTML puro
```html
<div style="text-align: center;">
    <h3>Código de validación electrónico</h3>
    <!-- Inyectando la URL con todos los colores y el texto directamente -->
    <img 
        src="https://api-qr.onrender.com/generar-qr?texto=https://mi-sistema.com/validar/98xcb72&fill_color=blue&back_color=yellow" 
        alt="QR de Validación" 
        width="200" 
        height="200"
    >
</div>
```

### ⚛️ Ejemplo para Frontend Moderno (React / Next.js)
```jsx
export default function TicketDigital() {
  const tokenCompra = "COMPRA-X-500-DOLARES-TOKEN-12345";
  const apiUrlBase = "https://api-qr.onrender.com/generar-qr";
  
  // TIPS: Las URLs deben codificarse para que los espacios y símbolos no dañen la petición web
  const textoCodificado = encodeURIComponent(tokenCompra);
  
  // Usamos el color corporativo azul marino de la empresa en Hexadecimal (#1e3a8a)
  // Nota: en la query URL el '#' se debe escapar a '%23'
  const finalImageSource = `${apiUrlBase}?texto=${textoCodificado}&fill_color=%231e3a8a`;

  return (
    <div className="card-ticket">
      <h2>Presenta este código al ingresar en taquilla:</h2>
      <img src={finalImageSource} alt="Ticket QR de Acceso" className="qr-image" />
    </div>
  );
}
```

### 🅰️ Ejemplo Componente Angular (`ticket.component.ts`)
```html
<!-- En tu template de Angular simplemente pasas la variable URL del entorno dinámicamente: -->
<div class="ticket-container">
  <h2>Escanea para ver tu factura online</h2>
  <img 
    [src]="'https://api-qr.onrender.com/generar-qr?texto=' + variableURLFactura + '&fill_color=green'" 
    alt="Factura Electrónica QR">
</div>
```

---

## 📘 Documentación Interactiva (Swagger UI)

Como bono, FastAPI autogenera documentación visual mientras trabajas en modo desarrollo. 
Si inicias el servidor de forma local con el comando `python -m uvicorn api:app --reload` y visitas:
* 👉 **http://localhost:8000/docs**
 
Podrás llenar y ver el funcionamiento y validar respuestas mediante un panel gráfico sin tener que escribir nada de código. Lo mismo ocurre en producción añadiendo el `/docs` al final de tu enlace `onrender.com`.
