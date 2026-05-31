# ─── Imports modules of project ────────────────────────────────
from models.patient import Patient
from models.staff import Doctor, Nurse
from modules.emergency  import EmergencyRoom
from modules.laboratory import Laboratory
from modules.pharmacy   import Medication, Pharmacy

from utils.cli import display_banner
from utils.storage import load_patients, load_staff, load_bills, save_patients, save_staff, save_bills

from ui.menus import (
    menu_patients, menu_staff, menu_emergency,
    menu_laboratory, menu_pharmacy, menu_billing
)

# ──────────────────────────────────────────────────────────────
#  Demo data loading functions
# ──────────────────────────────────────────────────────────────

def load_demo_data(patients: list, staff: list, pharmacy: Pharmacy) -> None:
    print("\n  Loading demo data...")
    p1 = Patient("Koné Ibrahim", 34, "Urgent")
    p1.triage_level = "P1"
    p2 = Patient("Ouédraogo Mariam", 58, "Hospitalized")
    p2.room_number = "12"
    patients.extend([p1, p2])
    
    staff.extend([
        Doctor("Diallo Moussa", "General Medicine"),
        Nurse("Kabore Sophie", "Surgery"),
        Doctor("Zongo Fatima", "Cardiothoracic"),
    ])
    
    load_pharmacy_demo(pharmacy)
    print("  ✓ Demo data loaded.\n")

def load_pharmacy_demo(pharmacy: Pharmacy) -> None:
    pharmacy.add_medication(Medication("Paracetamol 500mg", 150, 250.0))
    pharmacy.add_medication(Medication("Amoxicillin 1g", 8, 800.0))
    pharmacy.add_medication(Medication("Metformin 850mg", 45, 600.0))
    pharmacy.add_medication(Medication("Ibuprofen 400mg", 5, 350.0))

# ──────────────────────────────────────────────────────────────
#  Main application logic
# ──────────────────────────────────────────────────────────────

def main() -> None:
    """
    Main entry point for initializing and running the Hospital Management System.
    """
    display_banner()
    patients = load_patients()
    staff = load_staff()
    emergency_room = EmergencyRoom(1, 20)
    lab = Laboratory("Central Lab")
    pharmacy = Pharmacy("Central Pharmacy")
    invoices = load_bills(patients, staff)

    if not patients and not staff:
        load_demo_data(patients, staff, pharmacy)
    else:
        load_pharmacy_demo(pharmacy)

    for p in patients:
        if p.status == "Urgent":
            emergency_room.receive_patient(p)

    while True:
        print("\n" + "─" * 44)
        print("  MAIN MENU")
        print("─" * 44)
        print("  1. Patient Management")
        print("  2. Medical Staff")
        print("  3. Emergency Room")
        print("  4. Laboratory")
        print("  5. Pharmacy")
        print("  6. Billing")
        print("  7. Save & Quit")
        print("─" * 44)

        choice = input("  Choice: ").strip()

        if choice == "1": menu_patients(patients, emergency_room)
        elif choice == "2": menu_staff(staff, patients)
        elif choice == "3": menu_emergency(emergency_room, patients)
        elif choice == "4": menu_laboratory(lab, patients, staff)
        elif choice == "5": menu_pharmacy(pharmacy, patients, staff)
        elif choice == "6": menu_billing(patients, staff, invoices)
        elif choice == "7":
            save_patients(patients)
            save_bills(invoices)
            save_staff(staff)
            print("\n  Goodbye — System closed.\n")
            break
        else:
            print("  ✗ Invalid choice.")

if __name__ == "__main__":
    main()
