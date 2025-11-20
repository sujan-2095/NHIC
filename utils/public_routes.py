from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_user, current_user
import io
import os
import logging
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None
    logging.warning("PIL not available - image processing features will be disabled")

from db_handler import fetch_alerts, fetch_patient_by_id, fetch_visits_by_patient_id, log_action, insert_patient
from .auth import User
from .qr_utils import generate_qr

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    # Get all active alerts (from the last 14 days)
    from datetime import datetime, timedelta
    from db_handler import fetch_alerts
    
    alerts = fetch_alerts()
    # Filter only recent alerts (last 14 days)
    recent_alerts = []
    seen_alerts = set()  # To avoid duplicate alerts
    
    for alert in alerts:
        # Create a unique key for each alert to avoid duplicates
        alert_key = (alert['disease'], alert['district'])
        if alert_key not in seen_alerts:
            recent_alerts.append(alert)
            seen_alerts.add(alert_key)
    
    return render_template("home.html", alerts=recent_alerts)


@public_bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    from db_handler import insert_patient, fetch_patient_by_id as _fetch_patient_by_id
    import sqlite3

    if request.method == "POST":
        patient_id = request.form["patientId"]

        # Validate required fields
        required_fields = ["name", "age", "state", "district", "password", "user-input"]
        missing_fields = [field for field in required_fields if not request.form.get(field, "").strip()]
        if missing_fields:
            return render_template("register.html", error=f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate age is numeric
        try:
            age = int(request.form["age"])
            if age < 0 or age > 150:
                return render_template("register.html", error="Age must be between 0 and 150")
        except (ValueError, TypeError):
            return render_template("register.html", error="Age must be a valid number")

        if _fetch_patient_by_id(patient_id):
            return render_template(
                "register.html",
                error="Patient ID already exists. Change the last 6 digits or login if this is you.")

        qr_bytes, qr_b64 = generate_qr(patient_id)
        if not qr_bytes or not qr_b64:
            return render_template("register.html", error="Failed to generate QR code. Please try again.")
        try:
            qr_dir = os.path.join("static", "QR")
            os.makedirs(qr_dir, exist_ok=True)
            qr_path = os.path.join(qr_dir, f"{patient_id}_qr.png")
            with open(qr_path, "wb") as f:
                f.write(qr_bytes)
        except OSError as e:
            logging.warning(f"Failed to save QR code file for {patient_id}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error saving QR code for {patient_id}: {e}")

        data = {
            "id": patient_id,
            "name": request.form["name"].strip(),
            "age": age,  # Already validated above
            "state": request.form["state"].strip(),
            "district": request.form["district"].strip(),
            "password": request.form["password"],
            "qr_code": qr_bytes,
        }
        try:
            insert_patient(data)
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Patient ID already exists. Change the last 6 digits or login if this is you.")

        try:
            uid = None
            if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and hasattr(current_user, 'id'):
                uid = current_user.id
            log_action(f"New patient registered: {patient_id}", uid)
        except Exception as e:
            logging.warning(f"Failed to log patient registration: {e}")

        return render_template("register_success.html", patient_id=patient_id, qr_code=qr_b64)
    return render_template("register.html")


@public_bp.route("/scan")
def scan():
    # Temporary redirect to home until scan.html is implemented
    from flask import redirect
    return redirect(url_for("public.home"))


@public_bp.route("/fetch_patient", methods=["POST"])
def fetch_patient():
    # Validate JSON request
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON data"}), 400
            
        pid = data.get("patient_id")
        if not pid or not isinstance(pid, str) or not pid.strip():
            return jsonify({"status": "error", "message": "Valid patient_id is required"}), 400
            
        patient = fetch_patient_by_id(pid.strip())
        if not patient:
            return jsonify({"status": "error", "message": "Patient not found"}), 404
            
        visits = fetch_visits_by_patient_id(pid.strip())
        visits_data = [dict(v) for v in visits]
        return jsonify({"status": "success", "data": {"patient": dict(patient), "visits": visits_data}})
        
    except Exception as e:
        logging.error(f"Error fetching patient data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@public_bp.route("/qr_login", methods=["POST"])
def qr_login():
    # Validate JSON request
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON data"}), 400
            
        pid = data.get("patient_id")
        if not pid or not isinstance(pid, str) or not pid.strip():
            return jsonify({"status": "error", "message": "Valid patient_id is required"}), 400
            
        patient = fetch_patient_by_id(pid.strip())
        if not patient:
            return jsonify({"status": "error", "message": "Patient not found"}), 404

        log_user_id = None
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and hasattr(current_user, 'id'):
            log_user_id = current_user.id
            
        login_user(User(pid.strip(), "patient"), remember=True)
        log_action(f"Patient {pid.strip()} logged in via QR scan", log_user_id)
        
        return jsonify({
            "status": "success",
            "patient_name": patient["name"],
            "patient_id": pid.strip(),
            "redirect_url": url_for("patient.past_visits", patient_id=pid.strip())
        })
        
    except Exception as e:
        logging.error(f"Error during QR login: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@public_bp.route("/download_qr/<patient_id>")
def download_qr(patient_id: str):
    try:
        if not patient_id or not patient_id.strip():
            return ("Invalid patient ID", 400)
            
        patient = fetch_patient_by_id(patient_id.strip())
        if not patient:
            return ("Patient not found", 404)

        if not Image:
            return ("Image processing not available", 500)
            
        qr_bytes, _ = generate_qr(patient_id.strip())
        if not qr_bytes:
            return ("Failed to generate QR code", 500)
            
        buf_in = io.BytesIO(qr_bytes)
        img = Image.open(buf_in).convert("RGB")  # ensure no alpha for JPEG
        buf_out = io.BytesIO()
        img.save(buf_out, format="JPEG", quality=90)
        jpg_bytes = buf_out.getvalue()

        from flask import current_app
        response = current_app.response_class(
            jpg_bytes,
            mimetype='image/jpeg',
            headers={"Content-Disposition": f"attachment; filename={patient_id.strip()}_qr.jpg"}
        )
        return response
        
    except Exception as e:
        logging.error(f"Error generating QR download for patient {patient_id}: {e}")
        return ("Internal server error", 500)
