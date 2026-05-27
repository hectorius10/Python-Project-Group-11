from datetime import date
from typing import override

class Patient:
    """A class representing a patient in a healthcare system."""

    def __init__(self, name : str, age : int) -> None:
        self.__name: str = name
        self.__age: int = age
        self._medical_history: dict[date, str] = {}
        self.__blood_type: str = "Unknown"
        self._symptoms: list[str] = []
        self._current_diagnosis: str = ""
        self._fees_paid: float = 0.0

    def add_medical_history(self, diagnosis: str) -> None:
        """Add a medical diagnosis to the patient's history."""
        self._medical_history[date.today()] = diagnosis

    def calculate_fees(self, amount: float) -> None:
        """Add an amount to the patient's total fees paid."""
        self._fees_paid += amount

    @property
    def blood_type(self) -> str:
        """Get the patient's blood type."""
        return self.__blood_type

    @blood_type.setter
    def blood_type(self, blood_type: str) -> None:
        """Set the patient's blood type."""
        if blood_type not in ["A", "B", "AB", "O"]:
            raise ValueError("Invalid blood type. Must be one of: A, B, AB, O.")
        self.__blood_type = blood_type

    @override
    def __str__(self) -> str:
        return f"Patient(name={self.__name}, age={self.__age}, blood_type={self.__blood_type}, medical_history={self._medical_history}, symptoms={self._symptoms} , current_diagnosis={self._current_diagnosis})"



class UrgentPatient(Patient):
    """A class representing an urgent patient, which is a subclass of Patient."""

    LEVELS: dict[str, tuple[str, int]] = {
        "P1": ("Critique",    0),
        "P2": ("Urgent",      20),
        "P3": ("Semi-urgent", 60),
        "P4": ("Non urgent",  240),
    }

    emergency_fee: float = 5000.0

    def __init__(self, name: str, age: int, emergency_contact: str) -> None:
        super().__init__(name, age)
        self._triage_level: str = "P4"


    def get_priority(self) -> str:
        """Get the priority level of the urgent patient based on their triage level."""
        return self.LEVELS[self._triage_level][0]
    

    def calculate_fees(self, amount: float) -> None:
        """Add an amount to the urgent patient's total fees paid, including the emergency fee."""
        super().calculate_fees(amount=amount)

    def get_total_fees(self) -> float:
        """Calculate the total fees for the urgent patient, including the emergency fee."""
        return self._fees_paid + self.emergency_fee


    @override
    def __str__(self) -> str:
        return (f"{super().__str__()},"
                f" triage_level={self._triage_level},"
                f"priority={self.get_priority()})")
    


class HospitalizedPatient(Patient):
    """A class representing a hospitalized patient, which is a subclass of Patient."""

    def __init__(self, name: str, age: int, room_number: str) -> None:
        super().__init__(name, age)
        self._room_number: str = room_number
        self.__night_passes: int = 0
        
    def request_night_pass(self) -> None:
        """Request a night pass for the hospitalized patient."""
        self.__night_passes += 1

    def calculate_fees(self, amount: float) -> None:
        """Add an amount to the hospitalized patient's total fees paid."""
        super().calculate_fees(amount=amount)

    def get_total_fees(self) -> float:
        """Calculate the total fees for the hospitalized patient, including any additional fees for night passes."""
        night_pass_fee: float = 2500.0
        return self._fees_paid + (self.__night_passes * night_pass_fee)

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, room_number={self._room_number}, night_passes={self.__night_passes}) "

    
    

    
    
