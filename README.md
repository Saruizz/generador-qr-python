# 🔲 Generador de Códigos QR Interactivo

Una aplicación web moderna y rápida creada en Python con Streamlit para generar códigos QR personalizados en tiempo real. 

## 🚀 Características
- Generación de códigos QR instantánea al escribir.
- Personalización completa de los colores (Color de Frente y Fondo) del QR.
- Descarga en 1 clic: Guarda el resultado en formato PNG con la mejor calidad.
- Construido enteramente en Python usando las bibliotecas `qrcode` y `Pillow`.

## 📋 Requisitos Previos

Para ejecutar la aplicación en tu computadora, debes tener instalado **Python** (versión recomendada 3.8 o superior).

## 🛠 Instalación y Ejecución

Sigue estos mínimos pasos desde tu terminal (CMD, PowerShell o Git Bash):

### 1. Ubícate en la carpeta del proyecto
Abre tu terminal y navega hasta donde guardaste los archivos:
```bash
cd ruta/a/tu/carpeta/generador-qr-python
```

### 2. Instala las dependencias
Instala las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```
*(Es una buena práctica crear previamente un entorno virtual `venv`, aunque puedes ejecutarlas globalmente).*

### 3. Inicia la Aplicación Streamlit
Levanta el servidor local con el siguiente comando:
```bash
python -m streamlit run app.py
```

Tu navegador web predeterminado se abrirá automáticamente en la dirección `http://localhost:8501/` con el generador de QR listo para usar. 

---
> 🔒 **Nota Privacidad / Acceso en Red:**  
> Por defecto, Streamlit mostrará tu Generador a otras personas en tu misma red Wi-Fi mediante un "Network URL". Si deseas operar de modo completamente privado y restringir el servidor a tu computador, puedes ejecutar la aplicación así:  
> `python -m streamlit run app.py --server.address=localhost`
