import json
import os
from datetime import date

from models.patient import Patient
from models.staff import Doctor, Nurse

from services.billing import Invoice, save_bills, load_bills

DATA_PATIENTS: str = "data/patients.json"
DATA_STAFF:    str = "data/doctors.json"


def save_patients(patients: list[Patient]) -> None:
    """Save all patients to a JSON file, preserving all fields."""
    os.makedirs("data", exist_ok=True)
    data = [{
        "name":              p.name,
        "age":               p.age,
        "status":            p.status,
        "diagnosis":         p.current_diagnosis,
        "triage_level":      p.triage_level,
        "emergency_contact": p.emergency_contact,
        "room_number":       p.room_number,
        "medical_history":   p.medical_history,
    } for p in patients]
    with open(DATA_PATIENTS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n  ✓ {len(patients)} patient(s) saved → {DATA_PATIENTS}")


def load_patients() -> list[Patient]:
    """Load patients from JSON, restoring all fields correctly."""
    if not os.path.exists(DATA_PATIENTS):
        return []
    with open(DATA_PATIENTS, "r", encoding="utf-8") as f:
        data = json.load(f)
    patients = []
    for d in data:
        p = Patient(d["name"], d["age"], d.get("status", "Standard"))
        p.triage_level      = d.get("triage_level", "P4")
        p.emergency_contact = d.get("emergency_contact", "")
        p.room_number       = d.get("room_number", "")
        p.current_diagnosis = d.get("diagnosis", "None")
        p.medical_history   = d.get("medical_history", [])
        patients.append(p)
    return patients


def save_staff(staff: list) -> None:
    """Save all staff to JSON, preserving role, specialty and department."""
    os.makedirs("data", exist_ok=True)
    data = [{
        "name":       s.name,
        "role":       s.role,
        "specialty":  getattr(s, "specialty",  ""),
        "department": getattr(s, "department", ""),
    } for s in staff]
    with open(DATA_STAFF, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n  ✓ {len(staff)} staff member(s) saved → {DATA_STAFF}")


def load_staff() -> list:
    """Load staff from JSON, restoring Nurse vs Doctor correctly."""
    if not os.path.exists(DATA_STAFF):
        return []
    with open(DATA_STAFF, "r", encoding="utf-8") as f:
        data = json.load(f)
    staff = []
    for s in data:
        if s.get("role") == "Nurse":
            staff.append(Nurse(s["name"], s.get("department", "General")))
        else:
            staff.append(Doctor(s["name"], s.get("specialty", "General")))
    return staff


__all__ = [
    "save_patients", "load_patients",
    "save_staff",    "load_staff",
    "save_bills",    "load_bills",
]
