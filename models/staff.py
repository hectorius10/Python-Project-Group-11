from typing import override

class MedicalPersonnel:
    def __init__(self, name : str, role : str) -> None:
        self.name: str = name
        self.role: str = role

    @override
    def __str__(self) -> str:
        return f"{self.role}: {self.name}"

class Doctor(MedicalPersonnel):
    def __init__(self, name : str) -> None:
        super().__init__(name, role="Doctor")

        self.patients: list[str] = []
        self.diagnoses: dict[str, list[str]] = {}

    def heal(self, patient_name: str, diagnosis: str) -> None:
        """Diagnose a patient and add the diagnosis to their medical history."""
        print(f"Diagnosed {patient_name} with {diagnosis}.")

    def prescribe_medication(self, patient_name: str, medication: str) -> None:
        """Prescribe medication to a patient."""
        print(f"Prescribing {medication} to {patient_name}.")


    @override
    def __str__(self) -> str:
        return f"{super().__str__()}"

class Nurse(MedicalPersonnel):
    def __init__(self, name : str, department : str) -> None:
        super().__init__(name, role="Nurse")
        self.department: str = department
        self.assigned_patients: list[str] = []

    def assist_doctor(self, doctor_name: str, patient_name: str) -> None:
        """Assist a doctor with a patient."""
        print(f"Assisting Dr. {doctor_name} with patient {patient_name}.")

    def monitor_patient(self, patient_name: str) -> None:
        """Monitor a patient's condition."""
        print(f"Monitoring patient {patient_name}.")

    
    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, Department: {self.department}"


class Surgeon(Doctor):
    def __init__(self, name : str, specialty : str) -> None:
        super().__init__(name)

        self.specialty: str = "Surgery"

    def perform_surgery(self, patient_name: str, surgery_type: str) -> None:
        """Perform surgery on a patient."""
        print(f"Performing {surgery_type} surgery on {patient_name}.")

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, Role: {self.role}"        


class Dentist(Doctor):
    def __init__(self, name : str, specialty : str) -> None:
        super().__init__(name)

        self.speciality : str = "Dentist"

    def perform_dental_procedure(self, patient_name: str, procedure_type: str) -> None:
        """Perform a dental procedure on a patient."""
        print(f"Performing {procedure_type} dental procedure on {patient_name}.")

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, Role: {self.role}"


class Cardiologist(Doctor):
    def __init__(self, name : str) -> None:
        super().__init__(name)

        self.speciality : str = "Cardiology"

    def perform_heart_examination(self, patient_name: str) -> None:
        """Perform heart examination on a patient."""
        print(f"Performing heart examination on {patient_name}.")

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, Role: {self.role}"
