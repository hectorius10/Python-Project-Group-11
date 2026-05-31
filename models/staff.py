class MedicalPersonnel:
    """Base class representing all medical staff in the hospital.
    Defines the shared interface that every staff member must implement."""

    def __init__(self, name: str, role: str) -> None:
        """Initialize a medical personnel member with a name and role."""
        self.name: str = name
        self.role: str = role

    def treat(self, patient) -> str:
        """
        Treat a patient. This method is meant to be overridden by subclasses.
        """
        return f"{self.name} attends to {patient.name}"

    def __str__(self) -> str:
        """Return a string representation of the staff member."""
        return f"{self.role}: {self.name}"


class Doctor(MedicalPersonnel):
    """A doctor who can diagnose patients and prescribe medication.
    Inherits from MedicalPersonnel."""

    def __init__(self, name: str, specialty: str = "General") -> None:
        """Initialize a Doctor with a name and medical specialty."""
        super().__init__(name, role="Doctor")
        self.specialty: str = specialty

    def heal(self, patient, diagnosis: str) -> None:
        """Diagnose a patient and update their medical history."""
        patient.add_medical_history(diagnosis)
        patient.current_diagnosis = diagnosis
        print(f"    Dr {self.name} diagnosed {patient.name}: {diagnosis}")

    def prescribe_medication(self, patient_name: str, medication: str) -> str:
        """Prescribe medication to a patient."""
        return f"    Rx — Dr {self.name} prescribes {medication} to {patient_name}"

    def treat(self, patient) -> str:
        """Doctor's treatment: records a clinical note in the patient's history."""
        note = f"Clinical assessment by Dr {self.name} ({self.specialty})"
        patient.add_medical_history(note)
        return f"Dr {self.name} assessed {patient.name} [{self.specialty}]"

    def __str__(self) -> str:
        """Return a string representation of the doctor."""
        return f"Dr {self.name} ({self.specialty})"


class Nurse(MedicalPersonnel):
    """A nurse who monitors patients and administers routine care.
    Inherits from MedicalPersonnel."""

    def __init__(self, name: str, department: str = "General") -> None:
        """Initialize a Nurse with a name and department."""
        super().__init__(name, role="Nurse")
        self.department: str = department

    def monitor_patient(self, patient_name: str) -> None:
        """Monitor a specific patient and log the action."""
        print(f"    Nurse {self.name} monitoring {patient_name}")

    def treat(self, patient) -> str:
        """Nurse's treatment: records a monitoring note in the patient's history."""
        note = f"Monitoring and care by Nurse {self.name} ({self.department})"
        patient.add_medical_history(note)
        return f"Nurse {self.name} monitored {patient.name} [{self.department}]"

    def __str__(self) -> str:
        """Return a string representation of the nurse."""
        return f"Nurse {self.name} ({self.department})"
