class Patient:
    """A class representing a patient in the healthcare system."""

    def __init__(self, name: str, age: int, status: str = "Standard") -> None:
        """Initialize a new Patient with personal and medical information."""
        
        self._name:    str = name
        self._age:     int = age
        self._medical_history: list[str] = []

        self.status:            str = status   # Standard, Urgent
        self.blood_type:        str = "Unknown"
        self.current_diagnosis: str = "None"
        self.triage_level:      str = "P4"
        self.emergency_contact: str = ""
        self.room_number:       str = ""

    @property
    def name(self) -> str:
        """Get the patient's name. Read-only — prevents external modification."""
        return self._name

    @property
    def age(self) -> int:
        """Get the patient's age. Read-only — prevents external modification."""
        return self._age

    @property
    def medical_history(self) -> list[str]:
        """
        Get a copy of the patient's medical history.
        Returns a copy so external code cannot modify the list directly.
        """
        return self._medical_history.copy()

    @medical_history.setter
    def medical_history(self, value: list[str]) -> None:
        """
        Restore medical history from storage (load only).
        Should not be called outside of storage.py.
        """
        self._medical_history = value

    def add_medical_history(self, condition: str) -> None:
        """
        Add a medical condition or event to the patient's history.
        This is the only authorised way to write to the medical record.
        """
        self._medical_history.append(condition)

    def treat(self, staff_member) -> str:
        """
        Base treatment method — overridden by each staff subclass.
        Demonstrates polymorphism: same call, different behaviour per role.
        """
        return f"{staff_member.name} takes charge of {self._name}"

    def __str__(self) -> str:
        """Return a string representation of the patient."""
        return f"Patient({self._name}, {self._age}yo, {self.status})"
