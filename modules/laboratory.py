from datetime import date
from models.patient import Patient
from models.staff import Doctor


class LabResult:
    """
    Represents the result of a laboratory analysis, including value, unit,
    """

    STATUS_NORMAL:   str = "🟢 NORMAL"
    STATUS_ABNORMAL: str = "🟡 ABNORMAL"
    STATUS_CRITICAL: str = "🔴 CRITICAL"

    def __init__(self, parameter: str, value: float, unit: str,
                 min_norm: float, max_norm: float) -> None:
        """Initialize a lab result with parameter, value, unit, and norms."""
        self.parameter: str   = parameter
        self.value:     float = value
        self.unit:      str   = unit
        self.min_norm:  float = min_norm
        self.max_norm:  float = max_norm
        self.date:      date  = date.today()

    def get_status(self) -> str:
        """Evaluate and return the status based on the value vs norms."""
        if self.value < self.min_norm * 0.7 or self.value > self.max_norm * 1.5:
            return self.STATUS_CRITICAL
        elif self.value < self.min_norm or self.value > self.max_norm:
            return self.STATUS_ABNORMAL
        return self.STATUS_NORMAL

    def is_critical(self) -> bool:
        """Return True if the result is critical."""
        return self.get_status() == self.STATUS_CRITICAL

    def __str__(self) -> str:
        """Return a string representation of the lab result."""
        return (f"[{self.date}] {self.parameter}: "
                f"{self.value} {self.unit} "
                f"(norm: {self.min_norm}–{self.max_norm}) "
                f"→ {self.get_status()}")


class Analysis:
    """
    Represents a single laboratory analysis prescribed for a patient.
    """

    #Biological Standards : {parameter: (min, max, unit)}
    NORMS: dict[str, tuple[float, float, str]] = {
        "glycemia":      (0.70, 1.10, "g/L"),
        "hemoglobin":    (12.0, 17.0, "g/dL"),
        "creatinine":    (6.0,  12.0, "mg/L"),
        "platelets":     (150,  400,  "G/L"),
        "leukocytes":    (4.0,  10.0, "G/L"),
        "cholesterol":   (0.0,  2.0,  "g/L"),
        "temperature":   (36.1, 37.8, "°C"),
    }

    def __init__(self, patient: Patient, parameter: str, prescribed_by: Doctor) -> None:
        """Initialize an analysis with patient, parameter, and prescribing doctor."""
        if parameter not in self.NORMS:
            raise ValueError(
                f"Unknown parameter '{parameter}'. "
                f"Available: {list(self.NORMS.keys())}"
            )
        self.patient:        Patient      = patient
        self.parameter:      str          = parameter
        self.prescribed_by:  Doctor       = prescribed_by
        self.result:         LabResult | None = None
        self.date_prescribed: date        = date.today()

    def is_pending(self) -> bool:
        """Return True if no result has been entered yet."""
        return self.result is None

    def enter_result(self, value: float) -> LabResult:
        """
        Enter the measured value and generate a LabResult.
        Automatically alerts if the result is critical.
        """
        mini, maxi, unit = self.NORMS[self.parameter]
        self.result = LabResult(self.parameter, value, unit, mini, maxi)

    
        self.patient.add_medical_history(
            f"Lab result — {self.parameter}: {value} {unit} "
            f"({self.result.get_status()})"
        )

    
        if self.result.is_critical():
            print(f"\n    CRITICAL ALERT — {self.parameter} = {value} {unit}")
            print(f"    Patient  : {self.patient.name}")
            print(f"    Notify   : Dr {self.prescribed_by.name} immediately !")

        return self.result

    def __str__(self) -> str:
        """Return a string representation of the analysis."""
        status = str(self.result) if self.result else "⏳ Pending"
        return (f"Analysis({self.parameter}) — "
                f"Patient: {self.patient.name} | "
                f"Prescribed by: Dr {self.prescribed_by.name} | "
                f"{status}")


class Laboratory:
    """
    Manages all analyses, from prescription to result entry.
    Provides methods to check for pending and critical analyses.
    """
    def __init__(self, name: str) -> None:
        """Initialise le laboratoire avec son nom."""
        self.name:      str            = name
        self.analyses:  list[Analysis] = []
        self.nb_processed: int         = 0

    def prescribe(self, patient: Patient, parameter: str,
                  doctor: Doctor) -> Analysis:
        """Prescribe a new analysis for a patient."""
        analysis = Analysis(patient, parameter, doctor)
        self.analyses.append(analysis)
        print(f"    Analysis prescribed: {parameter} "
              f"for {patient.name} "
              f"by Dr {doctor.name}")
        return analysis

    def enter_result(self, analysis: Analysis, value: float) -> None:
        """Enter the result for a given analysis."""
        if analysis not in self.analyses:
            print("    Analysis not found in this laboratory.")
            return
        analysis.enter_result(value)
        self.nb_processed += 1

    def get_pending(self) -> list[Analysis]:
        """Return all analyses waiting for a result."""
        return [a for a in self.analyses if a.is_pending()]

    def get_critical(self) -> list[Analysis]:
        """Return all analyses with critical results."""
        return [a for a in self.analyses
                if not a.is_pending() and a.result.is_critical()]

    def check_alerts(self) -> None:
        """Display all critical results and pending analyses."""
        critical = self.get_critical()
        pending  = self.get_pending()

        print(f"\n  ═══ LAB ALERTS — {self.name} ═══")

        if critical:
            print(f"  🔴 {len(critical)} critical result(s):")
            for a in critical:
                print(f"    • {a}")
        else:
            print("  🟢 No critical results.")

        if pending:
            print(f"    {len(pending)} pending analysis(es):")
            for a in pending:
                print(f"    • {a}")
        else:
            print("    No pending analyses.")

    def display_all(self) -> None:
        """Display all analyses with their results."""
        print(f"\n  ═══ LABORATORY: {self.name} "
              f"({len(self.analyses)} analysis(es)) ═══")
        if not self.analyses:
            print("  No analyses recorded.")
            return
        for i, analysis in enumerate(self.analyses, 1):
            print(f"  {i}. {analysis}")
        print(f"\n  Processed today: {self.nb_processed}")

    def display_available_parameters(self) -> None:
        """Display all available analysis parameters with their norms."""
        print("\n  Available parameters:")
        for i, (param, (mini, maxi, unit)) in enumerate(Analysis.NORMS.items(), 1):
            print(f"    {i}. {param:<15} norm: {mini}–{maxi} {unit}")

    def __len__(self) -> int:
        """Return the total number of analyses."""
        return len(self.analyses)

    def __str__(self) -> str:
        """Return a string representation of the laboratory."""
        return (f"Laboratory({self.name} | "
                f"{len(self.analyses)} analyses | "
                f"{len(self.get_pending())} pending | "
                f"{len(self.get_critical())} critical)")
