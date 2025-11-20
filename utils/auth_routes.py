from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .auth import User
from db_handler import fetch_patient_by_id, log_action
import logging

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        try:
            uid = request.form.get("user_id", "").strip()
            pw = request.form.get("password", "")
            
            if not uid or not pw:
                return render_template("login.html", error="User ID and password are required")
            
            if uid == "admin" and pw == "admin123":
                login_user(User("admin", "admin"))
                log_action(f"Admin login: {uid}")
                return redirect(url_for("admin_dashboard"))
                
            patient = fetch_patient_by_id(uid)
            if patient and patient["password"] == pw:
                login_user(User(uid, "patient"))
                log_action(f"Patient login: {uid}")
                return redirect(url_for("past_visits", patient_id=uid))
                
            log_action(f"Failed login attempt for: {uid}")
            return render_template("login.html", error="Invalid credentials")
            
        except Exception as e:
            logging.error(f"Login error: {e}")
            return render_template("login.html", error="Login failed. Please try again.")
            
    return render_template("login.html")


@auth_bp.route("/logout", endpoint="logout")
@login_required
def logout():
    try:
        user_id = getattr(current_user, 'id', 'unknown') if hasattr(current_user, 'id') else 'unknown'
        logout_user()
        log_action(f"User logout: {user_id}")
    except Exception as e:
        logging.error(f"Logout error: {e}")
    return redirect(url_for("login"))


@auth_bp.route("/patient_login/<patient_id>", methods=["GET", "POST"], endpoint="patient_login")
def patient_login(patient_id: str):
    try:
        if not patient_id or not patient_id.strip():
            return redirect(url_for('public.home'))
            
        patient = fetch_patient_by_id(patient_id.strip())
        if not patient:
            return redirect(url_for('public.home'))

        if request.method == "POST":
            password = request.form.get("password", "")
            if not password:
                return render_template("login.html", patient_id=patient_id, error="Password is required")
                
            if patient["password"] == password:
                login_user(User(patient_id.strip(), "patient"))
                log_action(f"Patient direct login: {patient_id.strip()}")
                return redirect(url_for("past_visits", patient_id=patient_id.strip()))
            else:
                log_action(f"Failed patient login attempt: {patient_id.strip()}")
                return render_template("login.html", patient_id=patient_id, error="Invalid password")

        return render_template("login.html", patient_id=patient_id)
        
    except Exception as e:
        logging.error(f"Patient login error for {patient_id}: {e}")
        return redirect(url_for('public.home'))
