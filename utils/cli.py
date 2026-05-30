HOSPITAL_NAME: str = "Central Hospital of Ouagadougou"
VERSION:       str = "1.0.0"

def display_banner() -> None:
    """Display the application banner and version."""
    print("\n" + "═" * 54)
    print(f"   🏥  {HOSPITAL_NAME}")
    print(f"       Hospital Management System v{VERSION}")
    print("═" * 54)

def display_separator(title: str = "") -> None:
    """Display a section separator with optional title."""
    if title:
        print(f"\n  ── {title} ──")
    else:
        print(f"\n  {'─' * 44}")

def get_int_input(prompt: str) -> int:
    """Safely get an integer input from the user."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("    Please enter a valid number.")

def get_float_input(prompt: str) -> float:
    """Safely get a float input from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("    Please enter a valid amount.")

def choose_patient(patients: list) -> 'Patient | None':
    """Display patient list and let the user choose one."""
    if not patients:
        print("  No patients registered.")
        return None
    print()
    for i, p in enumerate(patients, 1):
        print(f"  {i}. {p.name} ({p.__class__.__name__})")
    idx = get_int_input("  Select patient number: ") - 1
    if 0 <= idx < len(patients):
        return patients[idx]
    print("    Invalid selection.")
    return None

def choose_doctor(staff: list) -> 'Doctor | None':
    """Display doctor list and let the user choose one."""
    from models.staff import Doctor
    doctors = [s for s in staff if isinstance(s, Doctor)]
    if not doctors:
        print("  No doctors registered.")
        return None
    print()
    for i, d in enumerate(doctors, 1):
        print(f"  {i}. Dr {d.name} ({d.__class__.__name__})")
    idx = get_int_input("  Select doctor number: ") - 1
    if 0 <= idx < len(doctors):
        return doctors[idx]
    print("  Invalid selection.")
    return None
