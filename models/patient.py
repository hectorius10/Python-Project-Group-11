class Patient:
    """A class representing a patient in the healthcare system."""

    def __init__(self, name: str, age: int, status: str = "Standard") -> None:
        """
        Initialize a new Patient.
        """
        self.name: str = name
        self.age: int = age
        self.status: str = status  # Standard, Urgent, Hospitalized
        self.medical_history: list[str] = []
        self.blood_type: str = "Unknown"
        self.current_diagnosis: str = "None"
        
        # Optional fields based on status
        self.triage_level: str = "P4" 
        self.emergency_contact: str = ""
        self.room_number: str = ""

    def add_medical_history(self, condition: str) -> None:
        """
        Add a medical condition or event to the patient's history.
        """
        self.medical_history.append(condition)

    def __str__(self) -> str:
        """
        Return a string representation of the patient.
        """
        return f"Patient({self.name}, {self.age}yo, {self.status})"
