import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# Configuración básica de la página de Streamlit
st.set_page_config(
    page_title="Generador de Códigos QR",
    page_icon="🔲",
    layout="centered"
)

# Título y descripción de la aplicación web
st.title("🔲 Generador de Códigos QR")
st.write("Ingresa un texto o URL para generar tu código QR al instante. Puedes personalizar los colores y descargar la imagen en formato PNG.")

# Campo de texto para que el usuario ingrese la información
# La interfaz se actualizará automáticamente (tiempo real) cada vez que el usuario escriba gracias al funcionamiento por defecto de Streamlit.
texto_usuario = st.text_input("Ingresa el texto o la URL:", placeholder="Ejemplo: https://www.google.com")

# Secciones de personalización visual organizadas en dos columnas
col_color1, col_color2 = st.columns(2)

with col_color1:
    # Selector de color para el QR (fill_color). Inicia en negro.
    color_frente = st.color_picker("Color del Código QR", "#000000")

with col_color2:
    # Selector de color para el fondo (back_color). Inicia en blanco.
    color_fondo = st.color_picker("Color de Fondo", "#FFFFFF")

# Lógica principal de generación: se ejecuta si hay texto ingresado
if texto_usuario:
    # Configuración de las propiedades geométricas y de tolerancia del objeto QRCode
    qr = qrcode.QRCode(
        version=1, # Controla el tamaño de la matriz (1 es 21x21)
        error_correction=qrcode.constants.ERROR_CORRECT_H, # Alta tolerancia a errores, útil si agregamos un logo al centro luego
        box_size=10, # Tamaño de cada "caja" o píxel visual del QR
        border=4, # Grosor del borde en cajas (4 es el mínimo estándar)
    )
    
    # Agregar los datos del usuario al objeto QR
    qr.add_data(texto_usuario)
    qr.make(fit=True)
    
    # Crear y renderizar la imagen del QR aplicando los colores seleccionados
    img = qr.make_image(fill_color=color_frente, back_color=color_fondo)
    
    # Para mostrar en web y preparar para descarga, manejamos la imagen temporalmente en memoria
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    imagen_bytes = buffer.getvalue()
    
    # Mostrar la imagen del código QR generado en la aplicación web
    st.markdown("### Resultado:")
    
    # Usamos columnas ficticias para centrar la imagen en la pantalla
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(imagen_bytes, caption="Código QR Generado", use_container_width=True)
        
        # Botón de descarga para guardar la imagen final en formato PNG
        st.download_button(
            label="Descargar Código QR",
            data=imagen_bytes,
            file_name="codigo_qr_generado.png",
            mime="image/png",
            use_container_width=True
        )
else:
    # Mensaje orientativo cuando el campo de texto está vacío
    st.info("El código QR se generará aquí automáticamente una vez que ingreses algún texto o URL.")
