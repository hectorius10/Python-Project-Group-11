from datetime import date
from models.patient import Patient
from models.staff import Doctor
import os

class Medication:
    """A class representing a medication managed by the pharmacy."""
    
    def __init__(self, name: str, stock: int, unit_price: float) -> None:
        """
        Initialize a new Medication instance.
        """
        self.name: str = name
        self.stock: int = stock
        self.unit_price: float = unit_price

    def dispense(self, quantity: int) -> bool:
        """
        Dispense a specific quantity of the medication.

        """
        if self.stock < quantity:
            print(f"  ✗ REFUSED: insufficient stock ({self.stock} available, {quantity} requested).")
            return False
        self.stock -= quantity
        return True

    def restock(self, quantity: int) -> None:
        """
        Add a specific quantity to the medication's stock.

        """
        self.stock += quantity
        print(f"  ✓ Restocked: {self.name} +{quantity} units (new stock: {self.stock})")

    def __str__(self) -> str:
        """
        Return a string representation of the medication details.

        """
        return f"{self.name:<25} Stock: {self.stock:>4} | Price: {self.unit_price:>8,.0f} FCFA"

class Prescription:
    """A class representing a medical prescription."""

    def __init__(self, patient: Patient, doctor: Doctor) -> None:
        """
        Initialize a new Prescription.

        """
        self.patient: Patient = patient
        self.doctor: Doctor = doctor
        self.date: date = date.today()
        self.items: list[tuple] = []  # (Medication, quantity, dosage)
        self.number: str = f"RX-{self.date.strftime('%Y%m%d')}-{patient.name[:3].upper()}"

    def add_medication(self, medication: Medication, quantity: int, dosage: str) -> None:
        """
        Add a medication with its quantity and dosage to the prescription.

        """
        self.items.append((medication, quantity, dosage))
        print(f"  ✓ Added to prescription: {medication.name} x{quantity} — {dosage}")

    def get_total_cost(self) -> float:
        """
        Calculate the total cost of all medications in the prescription.

        """
        return sum(med.unit_price * qty for med, qty, _ in self.items)

    def display(self) -> None:
        """
        Display a formatted summary of the prescription.
        """
        print(f"\n  PRESCRIPTION N° {self.number}")
        print(f"  Patient: {self.patient.name} | Doctor: Dr {self.doctor.name}")
        for med, qty, dosage in self.items:
            print(f"  - {med.name} x{qty} ({dosage}) : {med.unit_price * qty:,.0f} FCFA")
        print(f"  Total Cost: {self.get_total_cost():,.0f} FCFA")

    def export_to_txt(self) -> None:
        """
        Export the prescription details to a formatted text file in the 'data/ordonnances' directory.
        """
        os.makedirs("data/ordonnances", exist_ok=True)
        file_path = f"data/ordonnances/{self.number}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"PRESCRIPTION N° {self.number}\n")
            f.write(f"Date    : {self.date}\n")
            f.write(f"Patient : {self.patient.name}\n")
            f.write(f"Doctor  : Dr {self.doctor.name}\n")
            f.write("=" * 50 + "\n")
            f.write(f"{'MEDICATION':<22} {'QTY':>4}  {'DOSAGE':<20}\n")
            f.write("-" * 50 + "\n")
            for med, qty, dosage in self.items:
                f.write(f"{med.name:<22} {qty:>4}  {dosage:<20}\n")
            f.write("=" * 50 + "\n")
        print(f"   Prescription exported to {file_path}")

class Pharmacy:
    """A class representing the hospital pharmacy."""

    def __init__(self, name: str) -> None:
        """
        Initialize a new Pharmacy.

        """
        self.name: str = name
        self.stock: dict[str, Medication] = {}
        self.prescriptions: list[Prescription] = []

    def add_medication(self, medication: Medication) -> None:
        """
        Add a new medication to the pharmacy's stock.
        """
        self.stock[medication.name] = medication

    def get_medication(self, name: str) -> Medication | None:
        """
        Retrieve a medication from the stock by its name.
        """
        return self.stock.get(name, None)

    def create_prescription(self, patient: Patient, doctor: Doctor) -> Prescription:
        """
        Create and record a new prescription.
        """
        prescription = Prescription(patient, doctor)
        self.prescriptions.append(prescription)
        return prescription

    def display_stock(self) -> None:
        """
        Display the current stock of all medications in the pharmacy.
        """
        print(f"\n  ═══ STOCK — {self.name} ═══")
        if not self.stock:
            print("  No medications in stock.")
            return
        for med in self.stock.values():
            print(f"  • {med}")
