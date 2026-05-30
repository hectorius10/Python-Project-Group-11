from typing import override

class MedicalPersonnel:
    def __init__(self, name : str, role : str) -> None:
        self.name: str = name
        self.role: str = role

    @override
    def __str__(self) -> str:
        return f"{self.role}: {self.name}"

class Doctor(MedicalPersonnel):
    def __init__(self, name : str, specialty : str) -> None:
        super().__init__(name, role="Doctor")
        self.specialty: str = specialty
        self.patients: list[str] = []      

    def cure
    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, Specialty: {self.specialty}"

class Nurse(MedicalPersonnel):
    def __init__(self, name : str, department : str) -> None:
        super().__init__(name, role="Nurse")
        self.department: str = department
        self.assigned_patients: list[str] = []

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}, Department: {self.department}"

