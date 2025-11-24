"""
Módulo para geração de QR Codes
"""

import qrcode
import io
import base64


def gerar_qr_code_atendimento(token: str, host: str = 'localhost:5000') -> str:
    """
    Gera um QR Code para o atendimento do paciente.
    
    Args:
        token: Token único do atendimento
        host: Host da aplicação (ex: 'localhost:5000' ou 'example.com')
    
    Returns:
        String base64 da imagem do QR Code no formato data:image/png;base64,...
    """
    # Monta a URL completa para o app do paciente
    url = f"http://{host}/paciente/{token}"
    
    # Cria o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Gera a imagem
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converte para base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Retorna no formato data URI
    return f"data:image/png;base64,{img_str}"


def gerar_qr_code_url(url: str) -> str:
    """
    Gera um QR Code para qualquer URL.
    
    Args:
        url: URL completa
    
    Returns:
        String base64 da imagem do QR Code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"