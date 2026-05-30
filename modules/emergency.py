class EmergencyRoom:
    """Simplified Emergency Room acting as a basic FIFO queue."""

    def __init__(self, room_number: int, capacity: int) -> None:
        """
        Initialize a new Emergency Room.
        """
        self.room_number: int = room_number
        self.capacity: int = capacity
        self.queue: list = []
        self.treated_count: int = 0

    def receive_patient(self, patient) -> bool:
        """
        Receive a new patient into the emergency room queue.
        """
        if len(self.queue) >= self.capacity:
            print(f"   Emergency room {self.room_number} is full.")
            return False
        self.queue.append(patient)
        print(f"   {patient.name} added to emergency queue.")
        return True

    def treat_next(self):
        """
        Treat the next patient in the queue and update their medical history.
        """
        if not self.queue:
            print("   Queue is empty.")
            return None
        patient = self.queue.pop(0)
        self.treated_count += 1
        patient.add_medical_history(f"Treated in ER {self.room_number}")
        print(f"   Treating {patient.name}")
        return patient

    def display_status(self) -> None:
        """
        Display the current status of the emergency room, including the queue and capacity.
        """
        print(f"\n  ═══ EMERGENCY ROOM {self.room_number} ═══")
        print(f"  Waiting: {len(self.queue)}/{self.capacity}")
        for i, p in enumerate(self.queue, 1):
            print(f"    {i}. {p.name} [{p.triage_level}]")
