from flask import Blueprint, render_template, jsonify, url_for, request
from flask_login import login_required, current_user
from collections import Counter, defaultdict
import logging
from typing import Optional
from db_handler import (
    fetch_all_patients,
    fetch_all_visits_joined,
    fetch_alerts,
    fetch_logs,
    fetch_distinct_diseases,
    fetch_distinct_districts,
    fetch_distinct_hospitals,
    fetch_filtered_visits_joined,
    fetch_filtered_patients,
    fetch_patient_by_id,
)
import datetime
import io
from utils.config import WINDOW_DAYS
from utils.notifications import test_notification_system, send_system_notification

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/view_records", endpoint="view_records")
@login_required
def view_records():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403
    patients = fetch_all_patients()
    visits = fetch_all_visits_joined()
    return render_template("admin_all_visits.html", patients=patients, visits=visits)


@admin_bp.route("/registered_patients", endpoint="registered_patients")
@login_required
def registered_patients():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403
    patients = fetch_all_patients()
    return render_template("admin_registered_patients.html", patients=patients)


@admin_bp.route("/admin_dashboard", endpoint="admin_dashboard")
@login_required
def admin_dashboard():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403

    visits = fetch_all_visits_joined()
    alerts = fetch_alerts()

    # Visits by disease (case-insensitive aggregation, Title Case labels)
    vbd_map = Counter()
    disp_map_v = {}
    for v in visits:
        d = (v["disease"] or "").strip()
        key = d.lower()
        if not key:
            continue
        vbd_map[key] += 1
        disp_map_v[key] = d.title()
    labels_v = [disp_map_v[k] for k in sorted(vbd_map.keys())]
    data_v = [vbd_map[k] for k in sorted(vbd_map.keys())]
    visits_by_disease = { "labels": labels_v, "data": data_v }

    # Visits over time (per day)
    visits_by_day = defaultdict(int)
    for v in visits:
        ts = v["timestamp"]
        day = str(ts)[:10]  # YYYY-MM-DD
        visits_by_day[day] += 1
    visits_over_time = {
        "labels": sorted(visits_by_day.keys()),
        "data": [visits_by_day[d] for d in sorted(visits_by_day.keys())],
    }

    # Alerts aggregations (case-insensitive for disease)
    abd_map = Counter()
    disp_map_a = {}
    for a in alerts:
        d = (a["disease"] or "").strip()
        key = d.lower()
        if not key:
            continue
        abd_map[key] += 1
        disp_map_a[key] = d.title()
    alerts_by_district_counter = Counter([a["district"] for a in alerts])
    alerts_by_month_counter = Counter([a["month"] for a in alerts])

    alerts_by_disease = {
        "labels": [disp_map_a[k] for k in sorted(abd_map.keys())],
        "data": [abd_map[k] for k in sorted(abd_map.keys())],
    }
    # Top 10 districts by alerts
    top_districts = alerts_by_district_counter.most_common(10)
    alerts_by_district = {
        "labels": [d for d, _ in top_districts],
        "data": [c for _, c in top_districts],
    }
    # Order months Jan–Dec and fill zeros for missing
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    alerts_by_month = {
        "labels": month_names,
        "data": [alerts_by_month_counter.get(m, 0) for m in month_names],
    }

    return render_template(
        "admin_dashboard.html",
        visits_by_disease=visits_by_disease,
        visits_over_time=visits_over_time,
        alerts_by_disease=alerts_by_disease,
        alerts_by_district=alerts_by_district,
        alerts_by_month=alerts_by_month,
        window_days=WINDOW_DAYS,
    )


@admin_bp.route("/alerts", endpoint="view_alerts")
@login_required
def view_alerts():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403
    alerts = fetch_alerts()
    return render_template("alerts.html", alerts=alerts, window_days=WINDOW_DAYS)


@admin_bp.route("/system_logs", endpoint="system_logs")
@login_required
def system_logs():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403
    logs = fetch_logs()
    return render_template("system_logs.html", logs=logs)


@admin_bp.route("/api/check_alerts", endpoint="check_alerts")
@login_required
def check_alerts():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403
    except AttributeError:
        return jsonify({"error": "Unauthorized"}), 403

    # For demo purposes, return last 3 alerts
    recent_alerts = []
    alerts = fetch_alerts()
    for alert in alerts[:3]:
        recent_alerts.append({
            "disease": alert["disease"],
            "district": alert["district"],
            "count": alert["count"],
            "month": alert["month"],
        })

    return jsonify({"new_alerts": recent_alerts})


@admin_bp.route("/download_visits_xlsx", endpoint="download_visits_xlsx")
@login_required
def download_visits_xlsx():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403

    # Get filter parameters from request
    patient_id = request.args.get('patient_id', '').strip() or None
    patient_name = request.args.get('patient_name', '').strip() or None
    age_from = request.args.get('age_from', '').strip() or None
    age_to = request.args.get('age_to', '').strip() or None
    state = request.args.get('state', '').strip() or None
    district = request.args.get('district', '').strip() or None
    disease = request.args.get('disease', '').strip() or None
    location = request.args.get('location', '').strip() or None
    
    # Handle age interval filters
    age_min = None
    age_max = None
    if age_from:
        try:
            age_min = int(age_from)
        except (ValueError, TypeError):
            age_min = None
    if age_to:
        try:
            age_max = int(age_to)
        except (ValueError, TypeError):
            age_max = None

    # Use the database function for efficient filtering
    visits = fetch_filtered_visits_joined(
        disease=disease,
        district=district,
        state=state,
        patient_id=patient_id,
        location=location
    )
    
    # Apply additional filters that can't be done in SQL
    filtered_visits = []
    for visit in visits:
        # Convert sqlite3.Row to dict for modification
        visit_dict = dict(visit)
        
        # Get patient data for age filtering and display
        patient = fetch_patient_by_id(visit_dict['patient_id'])
        visit_dict['patient_age'] = patient['age'] if patient else None
        
        # Patient name filter (case-insensitive partial match)
        if patient_name and patient_name.lower() not in (visit_dict['patient_name'] or '').lower():
            continue
            
        # Age interval filter
        if visit_dict['patient_age'] is not None:
            if age_min is not None and visit_dict['patient_age'] < age_min:
                continue
            if age_max is not None and visit_dict['patient_age'] > age_max:
                continue
        elif age_min is not None or age_max is not None:
            # If we have age filters but no patient age, skip this visit
            continue
                
        filtered_visits.append(visit_dict)

    try:
        from openpyxl import Workbook
    except ImportError:
        logging.error("openpyxl dependency missing for Excel export")
        return ("Missing dependency: openpyxl. Activate your venv and run: pip install openpyxl", 500)

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Visits"

        headers = [
            "Visit ID", "Patient ID", "Patient Name", "Age", "State", "District", 
            "Hospital", "Doctor", "Disease", "Timestamp", "Has Prescription", "Has Scan"
        ]
        ws.append(headers)

        for v in filtered_visits:
            ws.append([
                v["visit_id"],
                v["patient_id"],
                v["patient_name"],
                v["patient_age"] or "N/A",
                v["state"],
                v["district"],
                v["hospital"],
                v["doctor"],
                v["disease"],
                v["timestamp"],
                "Yes" if v["has_prescription"] else "No",
                "Yes" if v["has_scan"] else "No",
            ])

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"filtered_visits_{ts}.xlsx" if any([patient_id, patient_name, age_from, age_to, state, district, disease]) else f"all_visits_{ts}.xlsx"
        
        from flask import current_app
        return current_app.response_class(
            buf.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logging.error(f"Error generating Excel file: {e}")
        return "Error generating Excel file", 500


@admin_bp.route("/download_patients_xlsx", endpoint="download_patients_xlsx")
@login_required
def download_patients_xlsx():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403

    # Get filter parameters from request
    patient_id = request.args.get('patient_id', '').strip() or None
    name = request.args.get('name', '').strip() or None
    age_from = request.args.get('age_from', '').strip() or None
    age_to = request.args.get('age_to', '').strip() or None
    state = request.args.get('state', '').strip() or None
    district = request.args.get('district', '').strip() or None
    
    # Handle age interval filters
    age_min = None
    age_max = None
    if age_from:
        try:
            age_min = int(age_from)
        except (ValueError, TypeError):
            age_min = None
    if age_to:
        try:
            age_max = int(age_to)
        except (ValueError, TypeError):
            age_max = None

    # Apply same filtering logic as filtered_patients
    patients = fetch_filtered_patients(
        state=state,
        district=district,
        age_min=age_min,
        age_max=age_max,
        name=name
    )
    
    # If patient_id is provided, filter by exact match
    if patient_id:
        patients = [p for p in patients if p["id"] == patient_id]

    try:
        from openpyxl import Workbook
    except ImportError:
        logging.error("openpyxl dependency missing for Excel export")
        return ("Missing dependency: openpyxl. Activate your venv and run: pip install openpyxl", 500)

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Registered Patients"

        headers = [
            "Patient ID", "Name", "Age", "State", "District"
        ]
        ws.append(headers)

        for patient in patients:
            ws.append([
                patient["id"],
                patient["name"],
                patient["age"],
                patient["state"],
                patient["district"]
            ])

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"filtered_patients_{ts}.xlsx" if any([patient_id, name, age_from, age_to, state, district]) else f"registered_patients_{ts}.xlsx"
        
        from flask import current_app
        return current_app.response_class(
            buf.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logging.error(f"Error generating Excel file: {e}")
        return "Error generating Excel file", 500


@admin_bp.route("/filtered_visits", endpoint="filtered_visits")
@login_required
def filtered_visits():
    from flask import request
    
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403

    # Get filter parameters from request
    patient_id = request.args.get('patient_id', '').strip() or None
    patient_name = request.args.get('patient_name', '').strip() or None
    age_from = request.args.get('age_from', '').strip() or None
    age_to = request.args.get('age_to', '').strip() or None
    state = request.args.get('state', '').strip() or None
    district = request.args.get('district', '').strip() or None
    disease = request.args.get('disease', '').strip() or None
    location = request.args.get('location', '').strip() or None
    
    # Handle age interval filters
    age_min = None
    age_max = None
    if age_from:
        try:
            age_min = int(age_from)
        except (ValueError, TypeError):
            age_min = None
    if age_to:
        try:
            age_max = int(age_to)
        except (ValueError, TypeError):
            age_max = None

    # Use the database function for efficient filtering
    visits = fetch_filtered_visits_joined(
        disease=disease,
        district=district,
        state=state,
        patient_id=patient_id,
        location=location
    )
    
    # Apply additional filters that can't be done in SQL
    filtered_visits = []
    for visit in visits:
        # Convert sqlite3.Row to dict for modification
        visit_dict = dict(visit)
        
        # Get patient data for age filtering and display
        patient = fetch_patient_by_id(visit_dict['patient_id'])
        visit_dict['patient_age'] = patient['age'] if patient else None
        
        # Patient name filter (case-insensitive partial match)
        if patient_name and patient_name.lower() not in (visit_dict['patient_name'] or '').lower():
            continue
            
        # Age interval filter
        if visit_dict['patient_age'] is not None:
            if age_min is not None and visit_dict['patient_age'] < age_min:
                continue
            if age_max is not None and visit_dict['patient_age'] > age_max:
                continue
        elif age_min is not None or age_max is not None:
            # If we have age filters but no patient age, skip this visit
            continue
                
        filtered_visits.append(visit_dict)

    return render_template(
        "admin_filtered_visits.html",
        visits=filtered_visits,
        current_filters={
            'patient_id': patient_id,
            'patient_name': patient_name,
            'age_from': age_from,
            'age_to': age_to,
            'state': state,
            'district': district,
            'disease': disease,
            'location': location
        }
    )


@admin_bp.route("/filtered_patients", endpoint="filtered_patients")
@login_required
def filtered_patients():
    from flask import request
    
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return "Unauthorized", 403
    except AttributeError:
        return "Unauthorized", 403

    # Get filter parameters from request
    patient_id = request.args.get('patient_id', '').strip() or None
    name = request.args.get('name', '').strip() or None
    age_from = request.args.get('age_from', '').strip() or None
    age_to = request.args.get('age_to', '').strip() or None
    state = request.args.get('state', '').strip() or None
    district = request.args.get('district', '').strip() or None
    
    # Handle age interval filters
    age_min = None
    age_max = None
    if age_from:
        try:
            age_min = int(age_from)
        except (ValueError, TypeError):
            age_min = None
    if age_to:
        try:
            age_max = int(age_to)
        except (ValueError, TypeError):
            age_max = None

    # Fetch filtered patients
    patients = fetch_filtered_patients(
        state=state,
        district=district,
        age_min=age_min,
        age_max=age_max,
        name=name
    )
    
    # If patient_id is provided, filter by exact match
    if patient_id:
        patients = [p for p in patients if p["id"] == patient_id]

    return render_template(
        "admin_filtered_patients.html",
        patients=patients,
        current_filters={
            'patient_id': patient_id,
            'name': name,
            'age_from': age_from,
            'age_to': age_to,
            'state': state,
            'district': district
        }
    )


@admin_bp.route("/api/filter_options", endpoint="api_filter_options")
@login_required
def api_filter_options():
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403
    except AttributeError:
        return jsonify({"error": "Unauthorized"}), 403

    option_type = request.args.get('type')
    
    if option_type == 'districts':
        districts = fetch_distinct_districts()
        return jsonify({"options": districts})
    elif option_type == 'diseases':
        diseases = fetch_distinct_diseases()
        return jsonify({"options": diseases})
    elif option_type == 'hospitals':
        hospitals = fetch_distinct_hospitals()
        return jsonify({"options": hospitals})
    elif option_type == 'states':
        patients = fetch_all_patients()
        states = sorted(list(set(p["state"] for p in patients if p["state"])))
        return jsonify({"options": states})
    else:
        return jsonify({"error": "Invalid option type"}), 400


@admin_bp.route("/test_notifications", endpoint="test_notifications")
@login_required
def test_notifications():
    """Test route for server-side notification system."""
    try:
        if not hasattr(current_user, 'role') or current_user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403
    except AttributeError:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        # Test the notification system
        success = test_notification_system()
        
        if success:
            # Also send a custom test notification
            send_system_notification(
                "Admin Test", 
                "Server-side notification system is working correctly!"
            )
            return jsonify({
                "success": True, 
                "message": "Test notifications sent successfully! Check your desktop for notifications."
            })
        else:
            return jsonify({
                "success": False, 
                "message": "Failed to send test notification. Check server logs for details."
            })
            
    except Exception as e:
        logging.error(f"Error testing notification system: {e}")
        return jsonify({
            "success": False, 
            "message": f"Error testing notification system: {str(e)}"
        }), 500
