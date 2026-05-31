import json
import os
import csv
from datetime import date, datetime

from models.patient import Patient
from models.staff import Doctor, Nurse
from modules.billing import Invoice

DATA_PATIENTS: str = "data/patients.json"
DATA_STAFF:    str = "data/doctors.json"
DATA_BILLS:    str = "data/bills.csv"


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
    data = []
    for s in staff:
        data.append({
            "name":       s.name,
            "role":       s.role,
            # ✅ Bug fix: department sauvegardé pour les nurses
            "specialty":  getattr(s, "specialty",  ""),
            "department": getattr(s, "department", ""),
        })
    with open(DATA_STAFF, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n  ✓ {len(staff)} staff member(s) saved → {DATA_STAFF}")


def load_staff() -> list:
    """
    Load staff from JSON.
    """
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


def save_bills(invoices: list[Invoice]) -> None:
    """Save all invoices to a CSV file."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_BILLS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Invoice Number", "Patient", "Doctor",
            "Date", "Total", "Paid", "Balance", "Status"
        ])
        for inv in invoices:
            d = inv.to_dict()
            writer.writerow([
                d["number"], d["patient"], d["doctor"],
                d["date"], d["total"], d["paid"],
                d["balance"], d["status"]
            ])
    print(f"\n  ✓ {len(invoices)} invoice(s) saved → {DATA_BILLS}")


def load_bills(patients: list[Patient], staff: list) -> list[Invoice]:
    """Load invoices from CSV and reconstruct Invoice objects."""
    if not os.path.exists(DATA_BILLS):
        return []
    invoices = []
    with open(DATA_BILLS, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patient = next(
                (p for p in patients if p.name == row["Patient"]),
                Patient(row["Patient"], 0)
            )
            doctor = next(
                (d for d in staff if d.name == row["Doctor"]),
                Doctor(row["Doctor"], "N/A")
            )
            inv = Invoice(patient, doctor)
            inv.number = row["Invoice Number"]
            try:
                inv.date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
            except ValueError:
                inv.date = date.today()
            total = float(row["Total"])
            if total > 0:
                inv.acts = []
                inv.add_act("Restored Balance", 1, total)
            paid = float(row["Paid"])
            if paid > 0:
                inv.make_payment(paid)
            invoices.append(inv)
    return invoices
