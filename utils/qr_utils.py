import io
import base64
import logging
from typing import Tuple, Optional

try:
    import qrcode
except ImportError:
    qrcode = None
    logging.error("qrcode library not available - QR code generation will fail")


def generate_qr(patient_id: str) -> Tuple[Optional[bytes], Optional[str]]:
    """Return (png_bytes, base64_str) for a QR encoding the given patient_id.
    
    Returns (None, None) if QR code generation fails.
    """
    try:
        if not qrcode:
            logging.error("QR code library not available")
            return None, None
            
        if not patient_id or not isinstance(patient_id, str) or not patient_id.strip():
            logging.error("Invalid patient_id provided for QR generation")
            return None, None
            
        qr = qrcode.QRCode(box_size=6, border=4)
        qr.add_data(patient_id.strip())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()
        qr_b64 = base64.b64encode(qr_bytes).decode("utf-8")
        return qr_bytes, qr_b64
        
    except Exception as e:
        logging.error(f"Error generating QR code for patient {patient_id}: {e}")
        return None, None
