from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import logging
from db_handler import (
    fetch_patient_by_id,
    fetch_visits_by_patient_id,
    fetch_visit_by_id,
    add_visit_record,
    insert_alert,
    count_unique_patients_in_window,
    find_existing_alert_in_window,
    update_alert_count,
    fetch_all_visits_joined,
    log_action,
)
import calendar
import datetime
from utils.config import WINDOW_DAYS, COMMON_ALERT_THRESHOLD, get_disease_options
from utils.notifications import send_alert_notification

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/past_visits/<patient_id>", methods=["GET", "POST"], endpoint="past_visits")
@login_required
def past_visits(patient_id: str):
    try:
        # Ensure logged-in user can only access their own records
        if hasattr(current_user, 'role') and current_user.role == "patient" and hasattr(current_user, 'id') and current_user.id != patient_id:
            return ("Unauthorized", 403)

        patient = fetch_patient_by_id(patient_id)
        if not patient:
            return redirect(url_for('public.home'))
        visits = fetch_visits_by_patient_id(patient_id)
        return render_template("past_visits.html", patient=patient, visits=visits)
    except Exception as e:
        logging.error(f"Error accessing past visits for patient {patient_id}: {e}")
        return ("Internal server error", 500)


@patient_bp.route("/patient_records/<patient_id>", methods=["GET"], endpoint="patient_records")
@login_required
def patient_records(patient_id: str):
    try:
        # Ensure logged-in user can only access their own records
        if hasattr(current_user, 'role') and current_user.role == "patient" and hasattr(current_user, 'id') and current_user.id != patient_id:
            return ("Unauthorized", 403)

        patient = fetch_patient_by_id(patient_id)
        if not patient:
            return redirect(url_for('public.home'))
        return render_template("patient_records.html", patient=patient)
    except Exception as e:
        logging.error(f"Error accessing patient records for patient {patient_id}: {e}")
        return ("Internal server error", 500)


@patient_bp.route("/add_visit/<patient_id>", methods=["GET", "POST"], endpoint="add_visit")
@login_required
def add_visit(patient_id: str):
    from flask import request, render_template

    try:
        patient = fetch_patient_by_id(patient_id)
        if not patient:
            return ("Patient not found", 404)
            
        if request.method == "POST":
            # Validate required fields
            hospital = request.form.get("hospital", "").strip()
            doctor = request.form.get("doctor", "").strip()
            disease = request.form.get("disease", "").strip()
            location = request.form.get("location", "").strip()
            
            if not all([hospital, doctor, disease]):
                disease_options = get_disease_options()
                return render_template("add_visit.html", patient=patient, disease_options=disease_options, error="Hospital, doctor, and disease are required")
            
            # If 'Other' selected, use the custom disease text
            if disease == 'Other':
                custom = request.form.get('disease_other', '').strip()
                if custom:
                    disease = custom
                else:
                    disease_options = get_disease_options()
                    return render_template("add_visit.html", patient=patient, disease_options=disease_options, error="Please specify the disease when selecting 'Other'")
            
            # Handle file uploads safely
            presc = None
            scan_doc = None
            
            if "prescription" in request.files and request.files["prescription"].filename:
                try:
                    presc = request.files["prescription"].read()
                except Exception as e:
                    logging.warning(f"Error reading prescription file: {e}")
                    
            if "scan_doc" in request.files and request.files["scan_doc"].filename:
                try:
                    scan_doc = request.files["scan_doc"].read()
                except Exception as e:
                    logging.warning(f"Error reading scan document file: {e}")
                    
            add_visit_record(patient_id, hospital, doctor, disease, presc, scan_doc, location if location else None)
            log_action(
                f"Visit added for patient {patient_id}",
                current_user.id if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and hasattr(current_user, 'id') else None,
            )

            # Outbreak detection (improved): unique patients per disease+district in last N days
            window_days = WINDOW_DAYS
            # Use a common threshold for all diseases (centralized)
            common_threshold = COMMON_ALERT_THRESHOLD

            unique_patients = count_unique_patients_in_window(disease, patient["district"], window_days)
            month = calendar.month_name[datetime.datetime.now().month]

            alert_generated = False
            if unique_patients >= common_threshold:
                existing = find_existing_alert_in_window(disease, patient["district"], window_days)
                if existing:
                    update_alert_count(existing["alert_id"], unique_patients)
                    action_msg = (
                        f"Alert updated: {disease} in {patient['district']} - {unique_patients} unique patients in last {window_days} days"
                    )
                else:
                    insert_alert(disease, patient["district"], month, unique_patients)
                    action_msg = (
                        f"Alert generated: {disease} in {patient['district']} - {unique_patients} unique patients in last {window_days} days"
                    )
                
                log_action(
                    action_msg,
                    current_user.id if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and hasattr(current_user, 'id') else None,
                )
                alert_generated = True
                
                # Send server-side desktop notification when alert is generated
                try:
                    notification_sent = send_alert_notification(
                        disease=disease,
                        district=patient["district"],
                        patient_count=unique_patients,
                        window_days=window_days
                    )
                    if notification_sent:
                        logging.info(f"Desktop notification sent for {disease} alert in {patient['district']}")
                    else:
                        logging.warning(f"Failed to send desktop notification for {disease} alert in {patient['district']}")
                except Exception as e:
                    logging.error(f"Error sending desktop notification: {e}")

            # Build disease options via centralized helper
            disease_options = get_disease_options()

            return render_template(
                "add_visit.html",
                patient=patient,
                success=True,
                alert_generated=alert_generated,
                alert_message=(
                    f"{disease} outbreak alert for {patient['district']}: {unique_patients} unique patient(s) in last {window_days} days"
                    if alert_generated else None
                ),
                disease_options=disease_options,
            )
        # GET: build disease options centrally
        disease_options = get_disease_options()
        return render_template("add_visit.html", patient=patient, disease_options=disease_options)
        
    except Exception as e:
        logging.error(f"Error adding visit for patient {patient_id}: {e}")
        return ("Internal server error", 500)


@patient_bp.route("/view_document/<int:visit_id>/<doc_type>", endpoint="view_document")
@login_required
def view_document(visit_id: int, doc_type: str):
    from flask import Response

    try:
        visit = fetch_visit_by_id(visit_id)
        if not visit:
            return ("Visit not found", 404)

        # Check authorization
        if hasattr(current_user, 'role') and current_user.role == "patient" and hasattr(current_user, 'id') and current_user.id != visit["patient_id"]:
            return ("Unauthorized", 403)

        doc_data = None
        filename = ""

        if doc_type == "prescription" and visit["prescription"]:
            doc_data = visit["prescription"]
            filename = f"prescription_{visit_id}"
        elif doc_type == "scan" and visit["scan_doc"]:
            doc_data = visit["scan_doc"]
            filename = f"scan_{visit_id}"

        if not doc_data:
            return ("Document not found", 404)

        # Detect file type based on content
        if doc_data.startswith(b'%PDF'):
            mimetype = 'application/pdf'
            filename += '.pdf'
        elif doc_data.startswith(b'\xff\xd8\xff'):
            mimetype = 'image/jpeg'
            filename += '.jpg'
        elif doc_data.startswith(b'\x89PNG'):
            mimetype = 'image/png'
            filename += '.png'
        elif doc_data.startswith(b'GIF'):
            mimetype = 'image/gif'
            filename += '.gif'
        else:
            # Try to serve as PDF by default
            mimetype = 'application/pdf'
            filename += '.pdf'

        return Response(
            doc_data,
            mimetype=mimetype,
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "no-cache",
            },
        )
        
    except Exception as e:
        logging.error(f"Error viewing document {doc_type} for visit {visit_id}: {e}")
        return ("Internal server error", 500)


@patient_bp.route("/download_document/<int:visit_id>/<doc_type>", endpoint="download_document")
@login_required
def download_document(visit_id: int, doc_type: str):
    from flask import Response

    try:
        visit = fetch_visit_by_id(visit_id)
        if not visit:
            return ("Visit not found", 404)

        # Check authorization
        if hasattr(current_user, 'role') and current_user.role == "patient" and hasattr(current_user, 'id') and current_user.id != visit["patient_id"]:
            return ("Unauthorized", 403)

        doc_data = None
        filename = ""

        if doc_type == "prescription" and visit["prescription"]:
            doc_data = visit["prescription"]
            filename = f"prescription_{visit_id}"
        elif doc_type == "scan" and visit["scan_doc"]:
            doc_data = visit["scan_doc"]
            filename = f"scan_{visit_id}"

        if not doc_data:
            return ("Document not found", 404)

        # Detect file type for extension
        if doc_data.startswith(b'%PDF'):
            mimetype = 'application/pdf'
            filename += '.pdf'
        elif doc_data.startswith(b'\xff\xd8\xff'):
            mimetype = 'image/jpeg'
            filename += '.jpg'
        elif doc_data.startswith(b'\x89PNG'):
            mimetype = 'image/png'
            filename += '.png'
        elif doc_data.startswith(b'GIF'):
            mimetype = 'image/gif'
            filename += '.gif'
        else:
            mimetype = 'application/octet-stream'

        return Response(
            doc_data,
            mimetype=mimetype,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache",
            },
        )
        
    except Exception as e:
        logging.error(f"Error downloading document {doc_type} for visit {visit_id}: {e}")
        return ("Internal server error", 500)


@patient_bp.route("/delete_visit/<int:visit_id>", methods=["POST"], endpoint="delete_visit")
@login_required
def delete_visit_route(visit_id: int):
    from flask import redirect, url_for
    from db_handler import delete_visit as delete_visit_db

    try:
        visit = fetch_visit_by_id(visit_id)
        if not visit:
            return ("Visit not found", 404)

        # Authorization: patients can delete their own visits; admins can delete any
        if hasattr(current_user, 'role'):
            if current_user.role == "patient":
                if not hasattr(current_user, 'id') or current_user.id != visit["patient_id"]:
                    return ("Unauthorized", 403)
            elif current_user.role != "admin":
                return ("Unauthorized", 403)
        else:
            return ("Unauthorized", 403)

        success = delete_visit_db(visit_id)
        if success:
            log_action(
                f"Visit {visit_id} deleted by {getattr(current_user, 'id', 'unknown')}",
                current_user.id if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and hasattr(current_user, 'id') else None,
            )
        return redirect(url_for("past_visits", patient_id=visit["patient_id"]))
        
    except Exception as e:
        logging.error(f"Error deleting visit {visit_id}: {e}")
        return ("Internal server error", 500)
