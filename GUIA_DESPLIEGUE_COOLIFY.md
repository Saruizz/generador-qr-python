# 🚀 Guía Completa de Despliegue: Coolify + OVHcloud + Cloudflare

Este proyecto ha sido preparado profesionalmente con una arquitectura multi-servicio basada en **Docker Compose**, lo que te permite desplegar de forma totalmente independiente tanto la interfaz interactiva de **Streamlit** como la **API REST de FastAPI** en un único servidor de **Coolify** administrado por ti.

---

## 🏗 Arquitectura del Despliegue

El archivo `docker-compose.yml` expone dos servicios contenerizados optimizados mediante el `Dockerfile` del proyecto:
1. **`app-web`** *(Puerto 8501)*: Interfaz de usuario en tiempo real creada con Streamlit.
2. **`api-rest`** *(Puerto 8001)*: Backend FastAPI listo para integraciones y consumo con Swagger UI (`/docs`).

---

## 🌐 Paso 1: Preparación del Servidor en OVHcloud

Para alojar **Coolify**, necesitarás un servidor en **OVHcloud** (puede ser una instancia de VPS, Public Cloud o servidor dedicado) con un sistema operativo compatible (recomendado **Ubuntu 22.04 LTS** o **Debian 12**).

### 1. Requisitos y Acceso por SSH
Conéctate por SSH al servidor de OVHcloud que recién creaste:
```bash
ssh root@<IP_DEL_SERVIDOR_OVH>
```

### 2. Instalación de Coolify
Coolify se instala con un único comando oficial. Ejecútalo en tu terminal SSH:
```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

> [!NOTE]
> El script instalará automáticamente Docker, Traefik (como proxy inverso oficial) y todas las dependencias necesarias de Coolify. Al finalizar, te proporcionará la dirección web local y el puerto para crear tu cuenta administrativa (ej. `http://<IP_DEL_SERVIDOR_OVH>:8000`).

---

## ☁️ Paso 2: Configuración de DNS y Seguridad en Cloudflare

Antes de realizar el despliegue en Coolify, debes preparar tus dominios o subdominios en **Cloudflare**.

### 1. Crear Registros DNS de Tipo A
En el panel de Cloudflare de tu dominio (ej. `tudominio.com`), añade dos registros DNS apuntando a la IP pública de tu servidor de OVHcloud:
* **Registro 1 (Para Streamlit UI):**
  * **Tipo:** `A` | **Nombre:** `qr` *(ej. qr.tudominio.com)* | **Contenido:** `IP_DEL_SERVIDOR_OVH` | **Proxy status:** Activo (Nube Naranja ☁️)
* **Registro 2 (Para FastAPI REST):**
  * **Tipo:** `A` | **Nombre:** `api.qr` *(ej. api.qr.tudominio.com)* | **Contenido:** `IP_DEL_SERVIDOR_OVH` | **Proxy status:** Activo (Nube Naranja ☁️)

### 2. Ajustes de SSL/TLS (¡Muy Importante!)
Ve a la sección **SSL/TLS** -> **Overview** en Cloudflare y selecciona el modo de encriptación:
* **Modo requerido:** `Full` o `Full (strict)`

> [!IMPORTANT]
> **Evitar bucles de redirección:** Coolify emitirá automáticamente certificados gratuitos de Let's Encrypt para tus dominios. Si dejas Cloudflare en modo *Flexible*, experimentarás un error `ERR_TOO_MANY_REDIRECTS`. Debe estar configurado en **Full** o **Full (strict)**.

### 3. Verificar WebSockets
Streamlit funciona transmitiendo eventos en tiempo real mediante **WebSockets** (`/_stcore/stream`). En Cloudflare, navega a **Network** y verifica que la opción **WebSockets** esté habilitada (por defecto viene activada en todas las cuentas).

---

## ⚡ Paso 3: Despliegue en Coolify

Con tus dominios apuntados y Coolify en marcha, procede a registrar el proyecto:

### 1. Conectar tu Repositorio Git
1. En el panel de Coolify, haz clic en **+ Add Resource** -> **New Project** -> **Production**.
2. Selecciona **Git Repository** (GitHub, GitLab, Bitbucket o Git autohospedado mediante clave SSH/HTTPS) y selecciona el repositorio `generador-qr-python`.

### 2. Seleccionar el Tipo de Build
* Cuando Coolify te pregunte el tipo de construcción o paquete, elige **Docker Compose** (Coolify leerá automáticamente tu archivo `docker-compose.yml`).

### 3. Configurar Dominios por Servicio (¡Importante para evitar Error 502!)
Al importar el proyecto, Coolify desglosará tus servicios y te permitirá asignar un **Dominio (URL)** para cada uno. 
Para asegurarte de que el proxy de Coolify (Traefik) envíe las peticiones al puerto interno correcto del contenedor y no recibas un **Error 502 Bad Gateway**, debes adjuntar el puerto interno de cada servicio al final de la URL en la casilla de dominio:

1. En la tarjeta de configuración del servicio **`app-web`**:
   * Introducir dominio: `https://qr.tudominio.com:8501`
   * *(Nota: El puerto `:8501` al final es una instrucción para que el proxy Traefik enpaquete el tráfico a ese puerto; tus visitantes entrarán de forma transparente a `https://qr.tudominio.com`)*
2. En la tarjeta de configuración del servicio **`api-rest`**:
   * Introducir dominio: `https://api.qr.tudominio.com:8001`
   * *(Dirige el tráfico exactamente al puerto `8001` del backend de Uvicorn)*

### 4. Iniciar el Despliegue
* Presiona el botón **Deploy** en la parte superior derecha. Coolify comenzará el proceso, clonará el código, construirá la imagen optimizada con el `Dockerfile` y expondrá de forma segura ambas URLs con HTTPS y certificado SSL operativo.

---

## 🛠 Detalles de los Archivos de Configuración Añadidos

Durante esta preparación, creamos en la raíz del proyecto tres ficheros esenciales:

1. **`Dockerfile`**:
   * Imagen base: `python:3.11-slim` (ligera y optimizada).
   * Variables de entorno para streaming de logs inalterado (`PYTHONUNBUFFERED=1`).
   * Instalación limpia de requerimientos (`requirements.txt`).
   * **Seguridad:** Configuración con usuario no privilegiado (`appuser`) para evitar ejecución como root dentro del contenedor.

2. **`.dockerignore`**:
   * Evita transferir entornos virtuales (`.venv`), cachés Python y el historial Git a la imagen final, reduciendo radicalmente los tiempos de build.

3. **`docker-compose.yml`**:
   * Orquesta los servicios `app-web` (UI) y `api-rest` (API).
   * **Optimización Streamlit:** Se han pasado los argumentos `--server.enableCORS=false` para garantizar compatibilidad sin caídas fortuitas con el túnel proxy de Cloudflare/Traefik.
   * **Optimización FastAPI:** Se han añadido los modificadores `--proxy-headers` y `--forwarded-allow-ips="*"` al comando de Uvicorn. Esto es fundamental para que FastAPI detecte correctamente la terminación HTTPS detrás de Cloudflare y Traefik, permitiendo que la consola interactiva **Swagger UI** (`/docs`) funcione sin errores de *Mixed Content*.

---

## ✅ Paso 4: Verificación Final

Una vez finalizada la construcción en Coolify, verifica la operatividad abriendo tus dominios en el navegador:

1. **Prueba de Interfaz Web:**  
   Ingresa a `https://qr.tudominio.com`. Debería cargar tu aplicación de Streamlit al instante y permitirte generar un QR en tiempo real.
2. **Prueba de API REST e Integración:**  
   Ingresa a `https://api.qr.tudominio.com/docs` para visualizar la consola Swagger y ejecutar pruebas del endpoint `/generar-qr` en vivo.
