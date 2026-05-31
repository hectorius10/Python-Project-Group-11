from models.patient import Patient
from models.staff import Doctor, Nurse
from modules.emergency import EmergencyRoom
from modules.laboratory import Laboratory
from modules.billing import Invoice
from modules.pharmacy import Pharmacy

from utils.cli import (
    display_separator, get_int_input, get_float_input,
    choose_patient, choose_doctor
)

def menu_patients(patients: list[Patient],
                  emergency_room: EmergencyRoom) -> None:
    """Submenu for patient management."""
    while True:
        display_separator("PATIENT MANAGEMENT")
        print("  1. Admit standard patient")
        print("  2. Admit urgent patient")
        print("  3. View all patients")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            name = input("  Name: ")
            age  = get_int_input("  Age : ")
            p    = Patient(name, age, "Standard")
            patients.append(p)
            print(f"  ✓ {p.name} registered.")

        elif choice == "2":
            name    = input("  Name             : ")
            age     = get_int_input("  Age              : ")
            contact = input("  Emergency contact: ")
            level   = input("  Triage (P1-P4)   : ").upper()
            p = Patient(name, age, "Urgent")
            p.triage_level      = level
            p.emergency_contact = contact
            patients.append(p)
            emergency_room.receive_patient(p)
            print(f"  ✓ {p.name} admitted to emergency [{level}].")

        elif choice == "3":
            if not patients:
                print("  No patients registered.")
                continue
            print(f"\n  {'─'*46}")
            print(f"  {'#':<4} {'NAME':<22} {'STATUS':<14} {'TRIAGE':>6}")
            print(f"  {'─'*46}")
            for i, p in enumerate(patients, 1):
                print(f"  {i:<4} {p.name:<22} {p.status:<14} "
                      f"{p.triage_level:>6}")
            print(f"  {'─'*46}")

        elif choice == "0":
            break


def menu_staff(staff: list, patients: list[Patient]) -> None:
    """Submenu for medical staff management."""
    while True:
        display_separator("MEDICAL STAFF")
        print("  1. View all staff")
        print("  2. Add a doctor")          
        print("  3. Add a nurse") 
        print("  4. Doctor heals a patient")
        print("  5. Nurse monitors a patient")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
        
            if not staff:
                print("  No staff registered.")
                continue
            print(f"\n  {'─'*44}")
            doctors = [s for s in staff if isinstance(s, Doctor)]
            nurses  = [s for s in staff if isinstance(s, Nurse)]
            if doctors:
                print(f"  DOCTORS ({len(doctors)})")
                for i, d in enumerate(doctors, 1):
                    print(f"    {i}. {d}")
            if nurses:
                print(f"  NURSES ({len(nurses)})")
                for i, n in enumerate(nurses, 1):
                    print(f"    {i}. {n}")
            print(f"  {'─'*44}")
            print(f"  Total: {len(staff)} staff member(s)")

        elif choice == "2":
    
            name      = input("  Doctor name      : ")
            specialty = input("  Specialty        : ")
            doctor    = Doctor(name, specialty)
            staff.append(doctor)
            print(f"    Dr {name} ({specialty}) added.")

        elif choice == "3":
    
            name       = input("  Nurse name       : ")
            department = input("  Department       : ")
            nurse      = Nurse(name, department)
            staff.append(nurse)
            print(f"    Nurse {name} ({department}) added.")

        elif choice == "4":
            doctor  = choose_doctor(staff)
            patient = choose_patient(patients)
            if doctor and patient:
                diagnosis = input("  Diagnosis: ")
                doctor.heal(patient, diagnosis)

        elif choice == "5":
            nurses = [s for s in staff if isinstance(s, Nurse)]
            if not nurses:
                print("  No nurses available.")
                continue
            print()
            for i, n in enumerate(nurses, 1):
                print(f"  {i}. {n}")
            idx = get_int_input("  Select nurse: ") - 1
            if 0 <= idx < len(nurses):
                patient = choose_patient(patients)
                if patient:
                    nurses[idx].monitor_patient(patient.name)

        elif choice == "0":
            break


def menu_emergency(emergency_room: EmergencyRoom,
                   patients: list[Patient]) -> None:
    """Submenu for emergency room management."""
    while True:
        display_separator("EMERGENCY ROOM")
        print("  1. View queue")
        print("  2. Treat next patient")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            emergency_room.display_status()
        elif choice == "2":
            emergency_room.treat_next()
        elif choice == "0":
            break

def menu_laboratory(lab: Laboratory, patients: list[Patient],
                    staff: list) -> None:
    """Submenu for laboratory management."""
    while True:
        display_separator("LABORATORY")
        print("  1. Prescribe analysis")
        print("  2. Enter result")
        print("  3. View all analyses")
        print("  4. Check alerts")
        print("  5. View available parameters")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            patient = choose_patient(patients)
            doctor  = choose_doctor(staff)
            if patient and doctor:
                lab.display_available_parameters()
                param = input("  Parameter: ").lower().strip()
                try:
                    lab.prescribe(patient, param, doctor)
                except ValueError as e:
                    print(f"    {e}")

        elif choice == "2":
            lab.display_all()
            pending = lab.get_pending()
            if not pending:
                print("  No pending analyses.")
                continue
            idx   = get_int_input("  Analysis number: ") - 1
            if 0 <= idx < len(pending):
                value = get_float_input("  Measured value : ")
                lab.enter_result(pending[idx], value)
            else:
                print("    Invalid number.")

        elif choice == "3":
            lab.display_all()

        elif choice == "4":
            lab.check_alerts()

        elif choice == "5":
            lab.display_available_parameters()

        elif choice == "0":
            break


def menu_pharmacy(pharmacy: Pharmacy, patients: list[Patient],
                  staff: list) -> None:
    """Submenu for pharmacy management."""
    while True:
        display_separator("PHARMACY")
        print("  1. View stock")
        print("  2. Create prescription")
        print("  3. Restock a medication")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            pharmacy.display_stock()

        elif choice == "2":
            patient = choose_patient(patients)
            doctor  = choose_doctor(staff)
            if patient and doctor:
                rx = pharmacy.create_prescription(patient, doctor)
                while True:
                    pharmacy.display_stock()
                    med_name = input(
                        "  Medication name (or DONE): "
                    ).strip()
                    if med_name.upper() == "DONE":
                        break
                    med = pharmacy.get_medication(med_name)
                    if not med:
                        print(f"   '{med_name}' not found.")
                        continue
                    qty    = get_int_input("  Quantity : ")
                    dosage = input("  Dosage   : ")
                    rx.add_medication(med, qty, dosage)
                rx.display()
                if input(
                    "\n  Export to text file? (y/n): "
                ).strip().lower() == "y":
                    rx.export_to_txt()

        elif choice == "3":
            pharmacy.display_stock()
            med_name = input("  Medication to restock: ").strip()
            med = pharmacy.get_medication(med_name)
            if med:
                qty = get_int_input("  Quantity to add: ")
                med.restock(qty)
            else:
                print(f"   '{med_name}' not found.")

        elif choice == "0":
            break

def menu_billing(patients: list, staff: list,
                 invoices: list) -> None:
    """Submenu for billing management."""
    while True:
        display_separator("BILLING")
        print("  1. Create invoice")
        print("  2. View all invoices")
        print("  3. Make a payment")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            patient = choose_patient(patients)
            doctor  = choose_doctor(staff)
            if patient and doctor:
                invoice = Invoice(patient, doctor)
                print(f"\n  Available acts: {list(Invoice.BASE_RATES.keys())}")
                while True:
                    act = input("  Add act (or DONE): ").strip()
                    if act.upper() == "DONE":
                        break
                    if act not in Invoice.BASE_RATES:
                        print(f"  ❌ Unknown act.")
                        continue
                    qty = get_int_input("  Quantity: ")
                    invoice.add_act(act, qty)
                invoice.display()
                invoices.append(invoice)

        elif choice == "2":
            if not invoices:
                print("  No invoices created yet.")
                continue
            print(f"\n  {'─' * 56}")
            for i, inv in enumerate(invoices, 1):
                status = "✅ Paid" if inv.is_paid() else "⏳ Pending"
                print(f"  {i}. {inv.number} | "
                      f"{inv.patient.name:<20} | "
                      f"Total: {inv.get_total():>8,.0f} | "
                      f"Balance: {inv.get_balance():>8,.0f} | "
                      f"{status}")
            print(f"  {'─' * 56}")

        elif choice == "3":
    
            if not invoices:
                print("  No invoices available.")
                continue
    
            pending = [inv for inv in invoices if not inv.is_paid()]
            if not pending:
                print("   All invoices are already paid.")
                continue
            print(f"\n  Pending invoices:")
            for i, inv in enumerate(pending, 1):
                print(f"  {i}. {inv.number} | "
                      f"{inv.patient.name} | "
                      f"Balance: {inv.get_balance():,.0f} FCFA")
            idx = get_int_input("  Select invoice: ") - 1
            if not (0 <= idx < len(pending)):
                print("   Invalid selection.")
                continue
            selected = pending[idx]
            selected.display()
    
            while not selected.is_paid():
                amount = get_float_input(
                    f"\n  Amount to pay "
                    f"(balance: {selected.get_balance():,.0f} FCFA): "
                )
                selected.make_payment(amount)
                if not selected.is_paid():
                    if input("  Pay more? (y/n): ").lower() != "y":
                        break

        elif choice == "0":
            break
