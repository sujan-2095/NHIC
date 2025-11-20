from flask import Flask, jsonify
from db_handler import init_db
import os
import secrets
import logging
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Auth initializer
from utils.auth import init_auth

# Blueprints
from utils.auth_routes import auth_bp
from utils.public_routes import public_bp
from utils.patient_routes import patient_bp
from utils.admin_routes import admin_bp

app = Flask(__name__)

# Use environment variable for secret key, fallback to hardcoded for development
secret_key = os.environ.get('FLASK_SECRET_KEY')
if not secret_key:
    # Development key - change this for production!
    secret_key = "dev-key-change-this-for-production-use-64-characters-minimum-length"
    logging.info("Using development secret key. Set FLASK_SECRET_KEY environment variable for production.")
app.secret_key = secret_key

# Initialize database and auth with error handling
try:
    init_db()
    init_auth(app)
except Exception as e:
    logging.error(f"Failed to initialize application: {e}")
    raise

# Register blueprints (no url_prefix to preserve routes)
app.register_blueprint(auth_bp)
app.register_blueprint(public_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(admin_bp)


# Global deployment route
@app.route('/api/deploy', methods=['POST'])
def deploy():
    """Deploy and push changes to GitHub repository"""
    try:
        # Change to project directory
        project_dir = r'c:\Users\SUJAN\Documents\Project\Sanitary\Code\V6'
        os.chdir(project_dir)
        
        # Git commands
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Auto deploy from Flask app'], check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
        
        logging.info("Successfully deployed and pushed to GitHub")
        return jsonify({"status": "success", "message": "Deployed and pushed to GitHub successfully"}), 200
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e}")
        return jsonify({"status": "error", "message": f"Deployment failed: {e}"}), 500
    except Exception as e:
        logging.error(f"Deployment error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Endpoint aliases to preserve legacy url_for calls without blueprint prefix
def _alias(endpoint_alias: str, real_endpoint: str, rule: str):
    if real_endpoint in app.view_functions:
        app.add_url_rule(rule, endpoint=endpoint_alias, view_func=app.view_functions[real_endpoint])


# Auth endpoints
_alias("login", "auth.login", "/login")
_alias("logout", "auth.logout", "/logout")
_alias("patient_login", "auth.patient_login", "/patient_login/<patient_id>")

# Public endpoints
_alias("home", "public.home", "/")
_alias("register", "public.register", "/register")
_alias("scan", "public.scan", "/scan")
_alias("fetch_patient", "public.fetch_patient", "/fetch_patient")
_alias("qr_login", "public.qr_login", "/qr_login")
_alias("download_qr", "public.download_qr", "/download_qr/<patient_id>")

# Patient endpoints
_alias("past_visits", "patient.past_visits", "/past_visits/<patient_id>")
_alias("patient_records", "patient.patient_records", "/patient_records/<patient_id>")
_alias("add_visit", "patient.add_visit", "/add_visit/<patient_id>")
_alias("view_document", "patient.view_document", "/view_document/<int:visit_id>/<doc_type>")
_alias("download_document", "patient.download_document", "/download_document/<int:visit_id>/<doc_type>")
_alias("delete_visit", "patient.delete_visit", "/delete_visit/<int:visit_id>")

# Admin endpoints
_alias("view_records", "admin.view_records", "/view_records")
_alias("registered_patients", "admin.registered_patients", "/registered_patients")
_alias("filtered_visits", "admin.filtered_visits", "/filtered_visits")
_alias("filtered_patients", "admin.filtered_patients", "/filtered_patients")
_alias("admin_dashboard", "admin.admin_dashboard", "/admin_dashboard")
_alias("view_alerts", "admin.view_alerts", "/alerts")
_alias("system_logs", "admin.system_logs", "/system_logs")
_alias("check_alerts", "admin.check_alerts", "/api/check_alerts")
_alias("api_filter_options", "admin.api_filter_options", "/api/filter_options")
_alias("download_visits_xlsx", "admin.download_visits_xlsx", "/download_visits_xlsx")
_alias("download_patients_xlsx", "admin.download_patients_xlsx", "/download_patients_xlsx")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
