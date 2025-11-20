# Centralized configuration for alert logic
# Adjust these values to update behavior across the system.

# Number of days to consider for outbreak detection window
WINDOW_DAYS: int = 14

# Common threshold for unique patients across all diseases
COMMON_ALERT_THRESHOLD: int = 2

# Default disease list used as fallback/seed. Final options should be DB-driven.
DEFAULT_DISEASE_OPTIONS = [
    "Dengue",
    "Malaria",
    "Typhoid",
    "Chikungunya",
    "Influenza",
    "COVID-19",
    "Tuberculosis",
    "Hepatitis",
    "Cholera",
]

def get_disease_options():
    """Return disease options driven by DB (distinct diseases) merged with defaults, plus 'Other'.

    Safe to import here because db_handler does not import config, avoiding cycles.
    """
    try:
        from db_handler import fetch_distinct_diseases
        db_vals = fetch_distinct_diseases() or []
    except Exception:
        db_vals = []
    # Normalize and dedupe case-insensitively, prefer Title Case for display
    def norm_list(values):
        out = {}
        for v in values:
            if not v:
                continue
            t = str(v).strip()
            if not t:
                continue
            key = t.lower()
            # Prefer Title Case display variant
            out[key] = t.title()
        return out

    merged_map = {}
    merged_map.update(norm_list(db_vals))
    merged_map.update(norm_list(DEFAULT_DISEASE_OPTIONS))

    merged = sorted(merged_map.values(), key=lambda s: s.lower())
    return [*merged, 'Other']
