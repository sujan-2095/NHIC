# Sanitary Health Management System - Comprehensive Documentation

## 1. Project Overview & Architecture
The Sanitary Health Management System is a comprehensive, centralized healthcare and epidemiological web application. It is purposefully designed to bridge the gap between patient record management and real-time public health monitoring. Built atop the reliable and lightweight **Flask web framework** in Python, it integrates an **SQLite3 relational database** to securely store medical data. 

At its core, this system not only digitizes legacy medical data (like handling patient history, uploaded disease prescriptions, and scans) but actively processes this data locally to identify potential disease epidemics. It evaluates recent hospital visit datasets over configurable rolling windows, tracking unique occurrences to automatically alert administrators about potential localized health crises.

It relies on a **Modular Blueprint Architecture**, separating the routing concerns across Auth, Public, Patient, and Admin layers, ensuring maintainability.

---

## 2. Core Functional Modules

### A. Patient Workflow & Authentication
* **Data Integration:** Patients securely log in using a designated Patient ID or scan an individualized system-generated **QR Code** (handled by `qrcode[pil]`).
* **Medical Dashboards:** Upon logging in, patients can view an chronological timeline of their past hospital visits.
* **Document Handling:** During any visit logging, doctors or admins can upload sensitive patient records—prescriptions and medical imaging/scans (e.g., X-Rays, MRIs). These are serialized and stored securely as `BLOB` datatypes within the SQLite database.

### B. Admin Dashboard & Deep Filtering
* **Macro-level Analytics:** The admin role has access to dynamic charting interfaces mapping the occurrences of distinct diseases mathematically distributed over varying geographic locations (states, districts) and timelines.
* **Granular Filtering Engine:** Provides multiple dropdowns filtering vast datasets by: state, district, disease category, presence of attached documents, hospital location, and patient age intervals.
* **Bulk Export Utility:** All filtered demographic profiles or aggregated patient visits can be exported identically to an MS Excel standard sheet (`.xlsx`) via the `openpyxl` backend library.

### C. Outbreak Detection Engine
The standout module is the proactive alert system built strictly into the transaction lifecycle:
* **Detection Logic:** It monitors specific geographic sectors (districts) and computes the number of *distinct individual patients* suffering from an identical illness (e.g., Dengue) within a localized time span (configured globally via `WINDOW_DAYS`, defaulting to 14 days).
* **Alert Trigger:** If occurrences exceed the `COMMON_ALERT_THRESHOLD` (default is 2 patients), an epidemiological alert is formally generated.
* **Notification Broadcasting:** Admins are notified of outbreaking situations by writing logic to standard application logs and by pushing **Direct Desktop Notifications** utilizing Python's `plyer` library. (Support exists for scalable SMTP email integration). 

### D. Automated Deployment Integration
A dedicated REST API endpoint `POST /api/deploy` is shipped for seamless CI/CD. It executes child subprocess scripts performing `git add`, `git commit`, and `git push` directly into the upstream repository `origin main`, ensuring rapid live pushing environment setups.

---

## 3. Database Schema Overview (SQLite)
File: `patient.db` | Handler: `db_handler.py`

| Table Name | Primary Schema Columns | Description |
| :--- | :--- | :--- |
| **`patients`** | `id` (PK, string), `name`, `age`, `state`, `district`, `qr_code` (BLOB) | Stores root user demographic data and encrypted auth records. |
| **`visits`** | `visit_id` (PK), `patient_id` (FK), `hospital`, `disease`, `location`, `timestamp` | Tracks every hospital encounter, storing disease classifications and time. |
| **`alerts`** | `alert_id` (PK), `disease`, `district`, `month`, `count`, `created_at` | Historical logging of all outbreak triggers. |
| **`logs`** | `log_id` (PK), `action`, `user`, `timestamp` | Auditing trail of structural systemic and administrative functions. |

*(Indexes actively maintain optimization specifically across `idx_visits_disease_ts` and `idx_patients_district` allowing high-speed outbreak queries).*

---

## 4. Sub-Component Network (Blueprints)
1. **`public_bp` (Public Routes):** `/`, `/register`, `/scan`, `/qr_login`
2. **`auth_bp` (Authentication Framework):** Admin login, session persistence validation.
3. **`patient_bp` (Patient Logic):** `/past_visits/<id>`, `/add_visit/<id>`, `/download_document` 
4. **`admin_bp` (Administrative Logic):** `/admin_dashboard`, `/filtered_visits`, `/system_logs`, `/download_visits_xlsx`, `/test_notifications`

---

## 5. Technical Requirements & Setup Instruction Guide
### Stack Dependencies (from `requirements.txt`)
* `flask>=3.0.0`
* `flask-login>=0.6.0`
* `python-dotenv>=1.0.0`
* `qrcode[pil]>=7.0.0`, `pillow>=10.0.0`
* `openpyxl>=3.1.0`
* `plyer>=2.1.0`

### Step-by-Step Installation
1. **Repository Access:**
   ```bash
   # Clone or position yourself within the root project directory:
   cd <project_directory>
   ```

2. **System Setup (Creating a virtual environment securely):**
   ```bash
   python -m venv .venv
   
   # Activation for Windows Command Prompt/Powershell:
   .venv\Scripts\activate
   # Activation for MacOS or Linux Terminals:
   source .venv/bin/activate
   ```

3. **Dependency Injection:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration (`.env` file):**
   Produce a `.env` in the root structure.
   ```env
   # Mandatory App Configuration Keys
   FLASK_SECRET_KEY=enter-a-robust-randomized-string-here
   APP_PORT=5000
   DEPLOY_PORT=5001
   ```

5. **Spin Up the Local Diagnostic Server:**
   ```bash
   python app.py
   ```
   *Note: Database auto-generation mechanisms are in place. The server natively listens over host `0.0.0.0` attached by default to port `5000` (`http://localhost:5000`). Make sure your firewall accepts inward TCP configurations if hosting on LAN.*
