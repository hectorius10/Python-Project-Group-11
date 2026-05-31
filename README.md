HospitalPro — Hospital Management System
HospitalPro is a terminal-based hospital management application built entirely

in Python. It allows hospital staff to manage patients, medical personnel,

emergency room queues, laboratory analyses, pharmacy stock, and patient billing

from a single interactive menu system.
All data is automatically saved to JSON files when the program closes and

reloaded on the next launch, so nothing is ever lost between sessions.

How to Run the Project
Requirements
·	Python 3.12 or higher
·	No external libraries — only Python standard library modules are used
Installation
# 1. Clone the repository
git clone https://github.com/your-group/hospitalpro.git
cd hospitalpro

# 2. Run the program from the project root
python main.py

The program must be launched from the project root folder.

Running it from inside a subfolder will break the relative imports.
First launch
On first launch, demo data is loaded automatically — two patients, three staff

members, and four medications — so you can explore every feature immediately

without entering anything manually.
Subsequent launches
Your saved data is restored from the data/ folder. The program picks up

exactly where you left off.

Features
·	Patient management — admit standard or urgent patients, assign triage

levels P1 to P4, record room numbers and emergency contacts, add notes to

medical records
·	Emergency room — FIFO queue that displays each patient's triage level;

urgent patients admitted via the menu are added to the queue automatically
·	Medical staff — add doctors with specialties and nurses with departments,

have a doctor diagnose a patient (updates their medical record), have a nurse

monitor a patient; polymorphism demonstrated live via treat()
·	Laboratory — prescribe biological analyses from a list of seven

parameters, enter measured values, receive automatic critical alerts when a

result falls outside the safe range
·	Pharmacy — manage medication stock, create prescriptions linked to a

patient and a doctor, add medications with quantity and dosage, export

prescriptions as formatted .txt files
·	Billing — create itemised invoices per patient visit using predefined act

rates, make partial or full payments, receive a clear alert when a payment

amount exceeds the remaining balance
·	Data persistence — patients, staff, and invoices saved to JSON on exit

and fully restored on reload; prescriptions exported as individual .txt

files in data/ordonnances/
·	Demo mode — if no saved data exists the system pre-loads sample records

so every module is immediately usable

Technologies Used
Module	Purpose
json	Saving and loading patients, staff, and invoices
os	Directory creation and file path checks
datetime	Recording dates on analyses, invoices, and prescriptions
csv	Legacy bill format (superseded by JSON)

No third-party packages are required. All modules are part of the Python

standard library.

Project Structure
hospitalpro/
│
├── main.py                  # Entry point — initialises all modules, loads
│                            # data, runs the main menu loop, saves on exit
│
├── models/
│   ├── patient.py           # Patient class — personal data, medical history,
│   │                        # triage level, room number, @property accessors
│   └── staff.py             # MedicalPersonnel (parent) → Doctor, Nurse
│                            # Polymorphic treat() method defined on all three
│
├── services/
│   ├── emergency.py         # EmergencyRoom — FIFO queue with capacity check;
│   │                        # updates patient history when treated
│   ├── laboratory.py        # LabResult, Analysis, Laboratory — prescribe
│   │                        # analyses, enter results, auto critical alerts
│   ├── pharmacy.py          # Medication, Prescription, Pharmacy — stock
│   │                        # management and .txt prescription export
│   └── billing.py           # Invoice — itemised acts, payments with balance
│                            # validation, JSON save/load
│
├── ui/
│   └── menus.py             # All interactive submenus: patients, staff,
│                            # emergency, laboratory, pharmacy, billing
│
├── utils/
│   ├── cli.py               # Shared UI helpers — banner, safe int/float
│   │                        # input, patient and doctor selectors
│   └── storage.py           # save/load functions for patients, staff,
│                            # invoices; re-exports billing save/load
│
└── data/                    # Created automatically on first save
    ├── patients.json        # All patient records with medical history
    ├── doctors.json         # All staff records with role and specialty
    ├── bills.json           # All invoices with itemised acts and payments
    └── ordonnances/         # One .txt file per exported prescription
        └── RX-*.txt


OOP Structure
models/patient.py
Class	Inherits from	Key methods
Patient	—	add_medical_history(), name (property), age (property), __str__()

Patient demonstrates encapsulation: _name, _age, and

_medical_history are protected attributes. External code reads name and

age through @property accessors and can only write to the medical record

through add_medical_history() — never by accessing the list directly.
Patient demonstrates abstraction: the internal structure of the medical

history list is hidden; callers only call add_medical_history() without

knowing how storage works.

models/staff.py
Class	Inherits from	Key methods
MedicalPersonnel	—	treat(), __str__()
Doctor	MedicalPersonnel	heal(), prescribe_medication(), treat(), __str__()
Nurse	MedicalPersonnel	monitor_patient(), treat(), __str__()

Doctor and Nurse both inherit from MedicalPersonnel, demonstrating

inheritance: name and role are defined once in the parent and reused

in both subclasses without duplication.
treat() is defined in MedicalPersonnel and overridden differently in

Doctor and Nurse, demonstrating polymorphism: the same method call

produces a clinical assessment note for a doctor and a monitoring note for a

nurse. Both write to the patient's medical record automatically.

services/emergency.py
Class	Inherits from	Key methods
EmergencyRoom	—	receive_patient(), treat_next(), display_status()

Manages a FIFO queue of urgent patients. When treat_next() is called it

removes the first patient from the queue and updates their medical record.

services/laboratory.py
Class	Inherits from	Key methods
LabResult	—	get_status(), is_critical(), __str__()
Analysis	—	is_pending(), enter_result(), __str__()
Laboratory	—	prescribe(), enter_result(), get_pending(), get_critical(), check_alerts(), display_all(), display_available_parameters(), __len__(), __str__()

LabResult evaluates a measured value against biological norms and returns

a status of NORMAL, ABNORMAL, or CRITICAL. Analysis links a Patient and

a Doctor to a specific parameter and updates the patient's medical record

when a result is entered. Laboratory manages all analyses and fires

automatic alerts for critical values.

services/pharmacy.py
Class	Inherits from	Key methods
Medication	—	dispense(), restock(), __str__()
Prescription	—	add_medication(), get_total_cost(), display(), export_to_txt()
Pharmacy	—	add_medication(), get_medication(), create_prescription(), display_stock()

Prescription links a Patient and a Doctor to a list of medications with

dosages. export_to_txt() writes a formatted ordonnance file to

data/ordonnances/.

services/billing.py
Class	Inherits from	Key methods
Invoice	—	add_act(), get_total(), get_balance(), is_paid(), make_payment(), display(), to_dict()

Invoice tracks all medical acts and payments for a single patient visit.

make_payment() validates the amount before accepting it and shows a clear

alert if the amount exceeds the remaining balance. to_dict() produces a

structured dictionary used for JSON persistence.

Acknowledgements
·	Python 3.12 official documentation: https://docs.python.org/3.12/
·	json module reference: https://docs.python.org/3/library/json.html
·	datetime module reference: https://docs.python.org/3/library/datetime.html
·	PEP 8 — Style Guide for Python Code: https://peps.python.org/pep-0008/
·	Python type hints: https://docs.python.org/3/library/typing.html

Group Members
Name	Github Profile
OUEDRAOGO Steve Christian Hector	github.com/hectorius10
OUEDRAOGO Rafa Nancy	github.com/ouedraogonancy-hue 
OUEDRAOGO G Reymond	github.com/ouedraogoreymond023-stack
KABORE Hortense	github.com/hortensekabore
OUEDRAOGO Hanifah	github.com/ouedraogohanifah01-afk
OUEDRAOGO Ratouswende Irene	github.com/ratouswendeirene-lgtm

