from datetime import date
from typing import override

class Patient:
    """A class representing a patient in a healthcare system."""

    def __init__(self, name : str, age : int) -> None:
        self.name: str = name
        self.age: int = age
        self._medical_history: dict[date, str] = {}
        self._blood_type: str = "Unknown"
        self.symptoms: list[str] = []
        self.current_diagnosis: str = ""
        self.fees_paid: float = 0.0

    def add_medical_history(self, diagnosis: str) -> None:
        """Add a medical diagnosis to the patient's history."""
        self._medical_history[date.today()] = diagnosis

    def calculate_fees(self, amount: float) -> None:
        """Calculate the patient's fees based on their medical history and current diagnosis."""
        self.fees_paid += amount

    @property
    def blood_type(self) -> str:
        """Get the patient's blood type."""
        return self._blood_type

    @blood_type.setter
    def blood_type(self, blood_type: str) -> None:
        """Set the patient's blood type."""
        if blood_type not in ["A", "B", "AB", "O"]:
            raise ValueError("Invalid blood type. Must be one of: A, B, AB, O.")
        self._blood_type = blood_type

    @override
    def __str__(self) -> str:
        return f"Patient(name={self.name}, age={self.age}, blood_type={self._blood_type}, medical_history={self._medical_history}, symptoms={self.symptoms} , current_diagnosis={self.current_diagnosis})"



class UrgentPatient(Patient):
    """A class representing an urgent patient, which is a subclass of Patient."""

    LEVELS: dict[str, tuple[str, int]] = {
        "P1": ("Critique",    0),
        "P2": ("Urgent",      20),
        "P3": ("Semi-urgent", 60),
        "P4": ("Non urgent",  240),
    }

    def __init__(self, name: str, age: int, emergency_contact: str) -> None:
        super().__init__(name, age)
        self.emergency_contact: str = emergency_contact
        self.triage_level: str = "P4"
    
    def calculate_fees(self, amount: float) -> None:
        self.fees_paid += amount + 5000  # Urgent patients have an additional fee of 5000

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, emergency_contact={self.emergency_contact})"

    


class HospitalizedPatient(Patient):
    """A class representing a hospitalized patient, which is a subclass of Patient."""

    def __init__(self, name: str, age: int, room_number: str) -> None:
        super().__init__(name, age)
        self.room_number: str = room_number
        self.night_passes: int = 0
        
    def request_night_pass(self) -> None:
        """Request a night pass for the hospitalized patient."""
        self.night_passes += 1

    def calculate_fees(self, amount: float) -> None:
        self.fees_paid += amount + (self.night_passes * 2500)  # Each night pass adds an additional fee of 2500

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, room_number={self.room_number}, night_passes={self.night_passes}) "

    
    

    
    
