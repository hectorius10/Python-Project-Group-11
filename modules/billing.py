from datetime import date
from models.patient import Patient
from models.staff import Doctor
import json
import os


class Invoice:
    """Tracks medical acts, payments and balance for a patient visit."""

    BASE_RATES: dict[str, float] = {
        "Consultation": 5_000.0,
        "Surgery":     75_000.0,
        "Lab Analysis":  8_000.0,
        "X-Ray":       15_000.0,
        "Emergency":   20_000.0,
        "Night Stay":  25_000.0,
        "Medication":   3_000.0,
    }

    def __init__(self, patient: Patient, doctor: Doctor) -> None:
        """Initialize a new Invoice for a specific patient and doctor."""
        self.patient:      Patient     = patient
        self.doctor:       Doctor      = doctor
        self.acts:         list[tuple] = []   # (description, quantity, price)
        self.amount_paid:  float       = 0.0
        self.date:         date        = date.today()
        self.number:       str         = (
            f"INV-{self.date.strftime('%Y%m%d')}"
            f"-{patient.name[:3].upper()}"
        )

    def add_act(self, description: str, quantity: int = 1,
                unit_price: float = None) -> None:
        """Add a medical act or service to the invoice."""
        price = unit_price if unit_price is not None \
            else self.BASE_RATES.get(description, 0.0)
        self.acts.append((description, quantity, price))
        print(f"   Added: {description} x{quantity} "
              f"— {price * quantity:,.0f} FCFA")

    def get_total(self) -> float:
        """Calculate the total cost of all acts."""
        return sum(qty * price for _, qty, price in self.acts)

    def get_balance(self) -> float:
        """Calculate the remaining balance to be paid."""
        return self.get_total() - self.amount_paid

    def is_paid(self) -> bool:
        """Return True if the invoice is fully paid."""
        return self.get_balance() <= 0

    def make_payment(self, amount: float) -> None:
        """
        Register a payment towards the invoice balance.
        """
        if amount <= 0:
            print("  ❌ Payment amount must be greater than zero.")
            return
        if self.is_paid():
            print("   This invoice is already fully paid.")
            return
        if amount > self.get_balance():
            print(f"\n  ❌ PAYMENT REFUSED")
            print(f"    Amount entered : {amount:>12,.0f} FCFA")
            print(f"    Balance remaining: {self.get_balance():>10,.0f} FCFA")
            print(f"    Maximum allowed  : {self.get_balance():>10,.0f} FCFA")
            print(f"  → Please enter an amount ≤ {self.get_balance():,.0f} FCFA")
            return 

        self.amount_paid += amount
        self.patient.add_medical_history(
            f"Payment of {amount:,.0f} FCFA "
            f"— Balance: {self.get_balance():,.0f} FCFA"
        )
        print(f"    Payment of {amount:,.0f} FCFA registered.")
        if self.is_paid():
            print(f"  ✅ Invoice {self.number} is now fully paid.")
        else:
            print(f"  Remaining balance: {self.get_balance():,.0f} FCFA")

    def display(self) -> None:
        """Display a formatted summary of the invoice."""
        w = 50
        print(f"\n  ╔{'═' * w}╗")
        print(f"  ║  INVOICE N° {self.number:<{w - 13}}║")
        print(f"  ║  Date    : {str(self.date):<{w - 12}}║")
        print(f"  ║  Patient : {self.patient.name:<{w - 12}}║")
        print(f"  ║  Doctor  : Dr {self.doctor.name:<{w - 15}}║")
        print(f"  ╠{'═' * w}╣")
        print(f"  ║  {'ACT':<26} {'QTY':>4}  {'UNIT':>7}  {'TOTAL':>8}  ║")
        print(f"  ╠{'─' * w}╣")
        for desc, qty, price in self.acts:
            print(f"  ║  {desc:<26} {qty:>4}  "
                  f"{price:>7,.0f}  {qty * price:>8,.0f}  ║")
        print(f"  ╠{'═' * w}╣")
        print(f"  ║  {'TOTAL':<34} {self.get_total():>10,.0f} F  ║")
        print(f"  ║  {'PAID':<34} {self.amount_paid:>10,.0f} F  ║")
        print(f"  ║  {'BALANCE':<34} {self.get_balance():>10,.0f} F  ║")
        status = "✅ PAID" if self.is_paid() else "⏳ PENDING"
        print(f"  ║  Status : {status:<{w - 11}}║")
        print(f"  ╚{'═' * w}╝")

    def to_dict(self) -> dict:
        """Convert the invoice to a structured dictionary for JSON export."""
        return {
            "number":  self.number,
            "date":    str(self.date),
            "patient": self.patient.name,
            "doctor":  self.doctor.name,
        
            "acts": [
                {
                    "description": desc,
                    "quantity":    qty,
                    "unit_price":  price,
                    "subtotal":    qty * price,
                }
                for desc, qty, price in self.acts
            ],
            "total":   self.get_total(),
            "paid":    self.amount_paid,
            "balance": self.get_balance(),
            "status":  "Paid" if self.is_paid() else "Pending",
        }


DATA_BILLS: str = "data/bills.json"


def save_bills(invoices: list[Invoice]) -> None:
    """
    Save all invoices to a JSON file.
    """
    os.makedirs("data", exist_ok=True)
    data = [inv.to_dict() for inv in invoices]
    with open(DATA_BILLS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n    {len(invoices)} invoice(s) saved → {DATA_BILLS}")


def load_bills(patients: list, staff: list) -> list[Invoice]:
    """
    Load invoices from JSON file and reconstruct Invoice objects.
    Restores acts, amounts and payment status correctly.
    """
    if not os.path.exists(DATA_BILLS):
        return []
    with open(DATA_BILLS, "r", encoding="utf-8") as f:
        data = json.load(f)
    invoices = []
    for d in data:
        patient = next(
            (p for p in patients if p.name == d["patient"]),
            Patient(d["patient"], 0)
        )
        doctor = next(
            (s for s in staff if s.name == d["doctor"]),
            Doctor(d["doctor"], "N/A")
        )
        inv = Invoice(patient, doctor)
        inv.number = d["number"]
    
        for act in d.get("acts", []):
            inv.add_act(
                act["description"],
                act["quantity"],
                act["unit_price"]
            )
        inv.amount_paid = d.get("paid", 0.0)
        invoices.append(inv)
    return invoices
