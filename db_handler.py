import os
import sqlite3
import logging
from typing import Optional, List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "patient.db")


def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                state TEXT,
                district TEXT,
                password TEXT,
                qr_code BLOB
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                hospital TEXT,
                doctor TEXT,
                disease TEXT,
                prescription BLOB,
                scan_doc BLOB,
                location TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease TEXT,
                district TEXT,
                month TEXT,
                count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Add location column to visits table if it doesn't exist (migration)
        try:
            conn.execute('ALTER TABLE visits ADD COLUMN location TEXT')
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Safe migration: add user column to logs if missing
        cur = conn.execute("PRAGMA table_info('logs')")
        cols = [row[1] for row in cur.fetchall()]
        if 'user' not in cols:
            conn.execute("ALTER TABLE logs ADD COLUMN user TEXT")

            # Helpful indexes for outbreak detection and lookups
            try:
                conn.execute("CREATE INDEX IF NOT EXISTS idx_visits_disease_ts ON visits(disease, timestamp)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_patients_district ON patients(district)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_visits_patient ON visits(patient_id)")
            except Exception as e:
                # Index creation failures are non-fatal
                logging.warning(f"Failed to create database indexes: {e}")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during database initialization: {e}")
        raise


def insert_patient(data: Dict[str, Any]) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT INTO patients (id, name, age, state, district, password, qr_code)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data["id"], data["name"], data["age"], data["state"],
                  data["district"], data["password"], data["qr_code"]))
            return True
    except sqlite3.IntegrityError as e:
        logging.warning(f"Patient insertion failed - integrity error: {e}")
        raise
    except sqlite3.Error as e:
        logging.error(f"Database error during patient insertion: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during patient insertion: {e}")
        raise


def fetch_all_patients() -> List[sqlite3.Row]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM patients").fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching patients: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching patients: {e}")
        return []


def fetch_patient_by_id(patient_id: str) -> Optional[sqlite3.Row]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching patient {patient_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching patient {patient_id}: {e}")
        return None


def add_visit_record(patient_id: str, hospital: str, doctor: str, disease: str, prescription: Optional[bytes], scan_doc: Optional[bytes], location: Optional[str] = None) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT INTO visits (patient_id, hospital, doctor, disease, prescription, scan_doc, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, hospital, doctor, disease, prescription, scan_doc, location))
            return True
    except sqlite3.Error as e:
        logging.error(f"Database error adding visit for patient {patient_id}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error adding visit for patient {patient_id}: {e}")
        raise


def fetch_visits_by_patient_id(patient_id: str) -> List[sqlite3.Row]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM visits WHERE patient_id = ?", (patient_id,)).fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching visits for patient {patient_id}: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching visits for patient {patient_id}: {e}")
        return []


def fetch_visit_by_id(visit_id: int) -> Optional[sqlite3.Row]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM visits WHERE visit_id = ?", (visit_id,)).fetchone()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching visit {visit_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching visit {visit_id}: {e}")
        return None


def log_action(action: str, user: Optional[str] = None) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Insert with user column; remains NULL if None
            conn.execute("INSERT INTO logs (action, user) VALUES (?, ?)", (action, user))
            return True
    except sqlite3.Error as e:
        logging.error(f"Database error logging action '{action}': {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error logging action '{action}': {e}")
        return False


def fetch_logs() -> List[sqlite3.Row]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM logs ORDER BY timestamp DESC").fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching logs: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching logs: {e}")
        return []


def insert_alert(disease: str, district: str, month: str, count: int) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT INTO alerts (disease, district, month, count)
                VALUES (?, ?, ?, ?)
            ''', (disease, district, month, count))
            return True
    except sqlite3.Error as e:
        logging.error(f"Database error inserting alert for {disease} in {district}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error inserting alert for {disease} in {district}: {e}")
        return False


def fetch_alerts() -> List[sqlite3.Row]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM alerts ORDER BY created_at DESC").fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching alerts: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching alerts: {e}")
        return []


def fetch_all_visits_joined() -> List[sqlite3.Row]:
    """Return all visits joined with patient name for display purposes."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(
                """
                SELECT v.visit_id, v.patient_id, p.name as patient_name, v.hospital, v.doctor, v.disease,
                       v.timestamp, v.prescription IS NOT NULL AS has_prescription,
                       v.scan_doc IS NOT NULL AS has_scan
                FROM visits v
                LEFT JOIN patients p ON p.id = v.patient_id
                ORDER BY v.timestamp DESC
                """
            ).fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching joined visits: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching joined visits: {e}")
        return []


def delete_visit(visit_id: int) -> bool:
    """Delete a visit by its visit_id."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("DELETE FROM visits WHERE visit_id = ?", (visit_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        logging.error(f"Database error deleting visit {visit_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error deleting visit {visit_id}: {e}")
        return False


def count_unique_patients_in_window(disease: str, district: str, window_days: int) -> int:
    """Count distinct patients for a disease in a district within the last N days.

    Joins visits with patients to use the authoritative district from patients table.
    """
    try:
        # Validate window_days is a positive integer
        if not isinstance(window_days, int) or window_days <= 0:
            logging.warning(f"Invalid window_days value: {window_days}")
            return 0
            
        window_expr = f"-{window_days} days"
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                '''
                SELECT COUNT(DISTINCT v.patient_id) as cnt
                FROM visits v
                JOIN patients p ON p.id = v.patient_id
                WHERE LOWER(v.disease) = LOWER(?)
                  AND p.district = ?
                  AND v.timestamp >= DATETIME('now', ?)
                ''',
                (disease, district, window_expr),
            )
            row = cur.fetchone()
            return int(row[0] if row and row[0] is not None else 0)
    except sqlite3.Error as e:
        logging.error(f"Database error counting patients for {disease} in {district}: {e}")
        return 0
    except Exception as e:
        logging.error(f"Unexpected error counting patients for {disease} in {district}: {e}")
        return 0


def find_existing_alert_in_window(disease: str, district: str, window_days: int) -> Optional[sqlite3.Row]:
    """Return the most recent alert for disease+district within the last N days, or None."""
    try:
        # Validate window_days is a positive integer
        if not isinstance(window_days, int) or window_days <= 0:
            logging.warning(f"Invalid window_days value: {window_days}")
            return None
            
        window_expr = f"-{window_days} days"
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(
                '''
                SELECT * FROM alerts
                WHERE LOWER(disease) = LOWER(?)
                  AND district = ?
                  AND created_at >= DATETIME('now', ?)
                ORDER BY created_at DESC
                LIMIT 1
                ''',
                (disease, district, window_expr),
            )
            return cur.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Database error finding alert for {disease} in {district}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error finding alert for {disease} in {district}: {e}")
        return None


def update_alert_count(alert_id: int, count: int) -> bool:
    """Update the count field of an existing alert."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("UPDATE alerts SET count = ? WHERE alert_id = ?", (count, alert_id))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        logging.error(f"Database error updating alert {alert_id}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error updating alert {alert_id}: {e}")
        return False


def fetch_distinct_diseases() -> List[str]:
    """Return a sorted list of distinct non-empty diseases recorded in visits."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                """
                SELECT DISTINCT TRIM(disease) AS d
                FROM visits
                WHERE disease IS NOT NULL AND TRIM(disease) <> ''
                ORDER BY d COLLATE NOCASE ASC
                """
            )
            rows = cur.fetchall()
            # rows are tuples; extract first column
            return [r[0] for r in rows if r and r[0]]
    except sqlite3.Error as e:
        logging.error(f"Database error fetching distinct diseases: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching distinct diseases: {e}")
        return []


def fetch_distinct_districts() -> List[str]:
    """Return a sorted list of distinct districts from patients."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                """
                SELECT DISTINCT TRIM(district) AS d
                FROM patients
                WHERE district IS NOT NULL AND TRIM(district) <> ''
                ORDER BY d COLLATE NOCASE ASC
                """
            )
            rows = cur.fetchall()
            return [r[0] for r in rows if r and r[0]]
    except sqlite3.Error as e:
        logging.error(f"Database error fetching distinct districts: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching distinct districts: {e}")
        return []


def fetch_distinct_hospitals() -> List[str]:
    """Return a sorted list of distinct hospitals from visits."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                """
                SELECT DISTINCT TRIM(hospital) AS h
                FROM visits
                WHERE hospital IS NOT NULL AND TRIM(hospital) <> ''
                ORDER BY h COLLATE NOCASE ASC
                """
            )
            rows = cur.fetchall()
            return [r[0] for r in rows if r and r[0]]
    except sqlite3.Error as e:
        logging.error(f"Database error fetching distinct hospitals: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching distinct hospitals: {e}")
        return []


def fetch_filtered_visits_joined(
    disease: Optional[str] = None,
    district: Optional[str] = None,
    hospital: Optional[str] = None,
    doctor: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    has_prescription: Optional[bool] = None,
    has_scan: Optional[bool] = None,
    patient_id: Optional[str] = None,
    state: Optional[str] = None,
    location: Optional[str] = None
) -> List[sqlite3.Row]:
    """Return filtered visits joined with patient name for display purposes."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            
            # Build the WHERE clause dynamically
            where_conditions = []
            params = []
            
            if disease:
                where_conditions.append("LOWER(v.disease) LIKE LOWER(?)")
                params.append(f"%{disease}%")
            
            if district:
                where_conditions.append("p.district = ?")
                params.append(district)
            
            if hospital:
                where_conditions.append("LOWER(v.hospital) LIKE LOWER(?)")
                params.append(f"%{hospital}%")
            
            if doctor:
                where_conditions.append("LOWER(v.doctor) LIKE LOWER(?)")
                params.append(f"%{doctor}%")
            
            if date_from:
                where_conditions.append("DATE(v.timestamp) >= ?")
                params.append(date_from)
            
            if date_to:
                where_conditions.append("DATE(v.timestamp) <= ?")
                params.append(date_to)
            
            if has_prescription is not None:
                if has_prescription:
                    where_conditions.append("v.prescription IS NOT NULL")
                else:
                    where_conditions.append("v.prescription IS NULL")
            
            if has_scan is not None:
                if has_scan:
                    where_conditions.append("v.scan_doc IS NOT NULL")
                else:
                    where_conditions.append("v.scan_doc IS NULL")
            
            if patient_id:
                where_conditions.append("v.patient_id = ?")
                params.append(patient_id)
            
            if state:
                where_conditions.append("p.state = ?")
                params.append(state)
            
            if location:
                where_conditions.append("LOWER(v.location) LIKE LOWER(?)")
                params.append(f"%{location}%")
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = f"""
                SELECT v.visit_id, v.patient_id, p.name as patient_name, v.hospital, v.doctor, v.disease,
                       v.timestamp, v.prescription IS NOT NULL AS has_prescription,
                       v.scan_doc IS NOT NULL AS has_scan, p.state, p.district, v.location
                FROM visits v
                LEFT JOIN patients p ON p.id = v.patient_id
                {where_clause}
                ORDER BY v.timestamp DESC
            """
            
            return conn.execute(query, params).fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching filtered visits: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching filtered visits: {e}")
        return []


def fetch_filtered_patients(
    state: Optional[str] = None,
    district: Optional[str] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    name: Optional[str] = None
) -> List[sqlite3.Row]:
    """Return filtered patients based on criteria."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            
            where_conditions = []
            params = []
            
            if state:
                where_conditions.append("state = ?")
                params.append(state)
            
            if district:
                where_conditions.append("district = ?")
                params.append(district)
            
            if age_min is not None:
                where_conditions.append("age >= ?")
                params.append(age_min)
            
            if age_max is not None:
                where_conditions.append("age <= ?")
                params.append(age_max)
            
            if name:
                where_conditions.append("LOWER(name) LIKE LOWER(?)")
                params.append(f"%{name}%")
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = f"""
                SELECT id, name, age, state, district
                FROM patients
                {where_clause}
                ORDER BY name ASC
            """
            
            return conn.execute(query, params).fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error fetching filtered patients: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching filtered patients: {e}")
        return []
