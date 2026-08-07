import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# Configuración básica de la página de Streamlit
st.set_page_config(
    page_title="Generador QR",
    layout="centered"
)

# Inyectar CSS y Google Material Icons para diseño premium UX
st.markdown("""
<style>
    /* Fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    /* Iconos profesionales (Material Symbols) sin usar emojis */
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .material-symbols-rounded {
        vertical-align: middle;
        margin-right: 8px;
        color: inherit;
    }

    /* Contenedor del encabezado */
    .header-container {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
    }
    
    /* Título principal con gradiente vibrante */
    .main-title {
        font-weight: 800;
        font-size: 3.2rem;
        background: linear-gradient(135deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    /* Para que el icono dentro del título mantenga el color sólido */
    .title-icon {
        font-size: 3.5rem; 
        color: #2563eb; 
        -webkit-text-fill-color: initial;
    }
    
    /* Subtítulo limpio */
    .subtitle {
        color: #64748b;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Títulos de sección */
    h4 {
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        color: #e2e8f0;
    }
    
    /* Ajustes sutiles para inputs (bordes redondeados) */
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 12px;
    }
    
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        opacity: 0.2;
    }
    
    /* Ocultar el botón de 'Deploy' y el menú superior nativo de Streamlit */
    .stDeployButton {
        display: none !important;
    }
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* =========================================
       CENTRADO ABSOLUTO (APLICA A TODAS LAS PANTALLAS)
       ========================================= */
       
    .main-title {
        font-size: 2.4rem;
        flex-direction: column;
        text-align: center;
        gap: 5px;
    }
    .title-icon {
        font-size: 3.5rem;
    }
    
    /* Centrar todos los encabezados (h4) */
    div[data-testid="stMarkdownContainer"] h4 {
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Forzar que las columnas se comporten de forma responsiva y centrada */
    div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    
    div[data-testid="column"] > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* CENTRADO DE COLOR PICKERS */
    [data-testid="stColorPicker"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        text-align: center !important;
    }
    [data-testid="stColorPicker"] label {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    [data-testid="stColorPicker"] label p {
        text-align: center !important;
        margin: 0 auto !important;
    }
    [data-testid="stColorPicker"] > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: max-content !important;
        margin: 0 auto !important;
    }
    
    /* CENTRADO DE CHECKBOX / TOGGLE */
    [data-testid="stCheckbox"], [data-testid="stToggle"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    [data-testid="stCheckbox"] > label, [data-testid="stToggle"] > label {
        display: flex !important;
        flex-direction: row !important; /* Mantener switch y texto lado a lado */
        align-items: center !important;
        justify-content: center !important;
        width: max-content !important;
        margin: 0 auto !important;
        gap: 8px !important;
    }
    [data-testid="stCheckbox"] p, [data-testid="stToggle"] p {
        text-align: center !important;
        margin: 0 !important;
    }

    /* CENTRADO DE TEXT INPUT LABELS */
    [data-testid="stTextInput"] label {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    [data-testid="stTextInput"] label p {
        text-align: center !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado UI
st.markdown("""
<div class="header-container">
    <div class="main-title">
        <span class="material-symbols-rounded title-icon">qr_code_2</span>
        Generador QR
    </div>
    <div class="subtitle">Crea códigos QR personalizados de alta resolución en un instante.</div>
</div>
""", unsafe_allow_html=True)

# Sección de Entrada de Datos
st.markdown('<h4><span class="material-symbols-rounded">link</span> Contenido del Enlace</h4>', unsafe_allow_html=True)
texto_usuario = st.text_input("Ingresa la URL o el texto a codificar:", placeholder="Ejemplo: https://www.google.com", label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)

# Sección de Personalización visual
st.markdown('<h4><span class="material-symbols-rounded">palette</span> Personalización Visual</h4>', unsafe_allow_html=True)
col_color1, col_color2 = st.columns(2)

with col_color1:
    color_frente = st.color_picker("Color del Patrón", "#000000")

with col_color2:
    # Agrupamos en sub-columnas con alineación inferior nativa de Streamlit
    sub_col1, sub_col2 = st.columns([1, 1.2], vertical_alignment="bottom")
    
    with sub_col2:
        fondo_transparente = st.toggle("Transparente", value=False)
        
    with sub_col1:
        color_fondo_picker = st.color_picker("Color de Fondo", "#FFFFFF", disabled=fondo_transparente)
        
    color_fondo = "transparent" if fondo_transparente else color_fondo_picker

st.markdown("<hr>", unsafe_allow_html=True)

# Lógica principal de generación
if texto_usuario:
    # Generación del QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12, # Resolución incrementada de 10 a 12 para mayor nitidez
        border=4,
    )
    
    qr.add_data(texto_usuario)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=color_frente, back_color=color_fondo)
    
    # Manejo en memoria
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    imagen_bytes = buffer.getvalue()
    
    # UI del Resultado
    st.markdown('<h4 style="text-align: center;"><span class="material-symbols-rounded">download_done</span> Tu Código QR</h4>', unsafe_allow_html=True)
    
    # Centrado del QR
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(imagen_bytes, use_container_width=True)
        
        # Botón de descarga con énfasis visual primario
        st.download_button(
            label="Descargar Imagen PNG",
            data=imagen_bytes,
            file_name="codigo_qr_premium.png",
            mime="image/png",
            type="primary", 
            use_container_width=True
        )
else:
    # Mensaje orientativo limpio (sin emojis)
    st.info("Introduce un texto o enlace en la parte superior para previsualizar tu código QR.")
