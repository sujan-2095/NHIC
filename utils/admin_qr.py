# admin_qr_generator.py
import os
import qrcode

def generate_admin_qr(output_path="static/QR/admin_qr.png"):
    # Ensure target directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create QR for the literal string 'admin'
    img = qrcode.make("admin")  # requires 'qrcode' and Pillow
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    path = generate_admin_qr()
    print(f"Admin QR saved to: {path}")