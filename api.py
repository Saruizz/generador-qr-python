from fastapi import FastAPI, Response, Query
from fastapi.responses import HTMLResponse
import qrcode
from io import BytesIO

app = FastAPI(
    title="Generador de Códigos QR API",
    description="API para generar códigos QR sobre la marcha e integrarlos en otros sistemas.",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>QR API</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>API de Generador de Códigos QR</h1>
            <p>El servicio está corriendo correctamente.</p>
            <p>Ve a <a href="/docs">/docs</a> para ver la documentación interactiva y probar los endpoints.</p>
        </body>
    </html>
    """

@app.get("/generar-qr")
def generar_qr(
    texto: str = Query(..., description="El texto o URL a codificar en el QR"),
    fill_color: str = Query("black", description="Color del patrón del QR (ej: black, red, #000000)"),
    back_color: str = Query("white", description="Color del fondo del QR (ej: white, transparent, #FFFFFF)")
):
    """
    Genera un código QR y lo devuelve directamente como una imagen PNG.
    Ideal para incrustar directamente en etiquetas <img> HTML.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(texto)
    qr.make(fit=True)
    
    # Intentar interpretar los colores. Si falla (color no válido), usar blanco y negro básicos.
    try:
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
    except ValueError:
        img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar en memoria
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    imagen_bytes = buffer.getvalue()
    
    # Retornamos la respuesta indicando que el contenido es directamente una imagen
    return Response(content=imagen_bytes, media_type="image/png")
