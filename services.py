from models import Doctor, Patient, Pharmacist

class Digital_Prescription:
    def __init__(self):
        self.doctors: list[Doctor] = []
        self.prescriptions: list[Prescription] = []
        self.patients: list[Patient] = []

        self._next_prescription_id = 1
        self._seed_demo_data()

    def _seed_demo_data(self) -> None:
        # Doctors
        self.doctors.append(Doctor("Nick", "Gkizis", "nickG", "Pathologist", "licence100"))
        self.doctors.append(Doctor("Joanah", "Pavlou", "joanahP", "Cardiologist", "licence200"))
        self.doctors.append(Doctor("Bruce", "Dickinson", "bruceD", "ENT", "licence300"))

        # Patients
        self.patients.append(Patient("Pavlina", "Ioannou", "pavlinaIoannou", "amka100", True, "Athens", "6900000000", "EFKA"))
        self.patients.append(Patient("George", "Konstantinou", "georgeKonstantinou", "amka200", False, "Thessaloniki", "6911111111", "IKA"))
        self.patients.append(Patient("Maria", "Papadopoulou", "mariaPapadopoulou", "amka300", True, "Patra", "6922222222", "OGA"))

    # General Functions
    def find_doctor(self, license_id: str) -> Doctor | None:
        return next((d for d in self.doctors if d.medical_license_id == license_id), None)

    def find_drug(self, barcode: str) -> Drug | None:
        return next((d for d in self.drugs if d.barcode == barcode), None)

    def find_patient(self, amka: str) -> Patient | None:
        return next((p for p in self.patients if p.amka == amka), None)

    #Functions Ιατρού

    def create_prescription(self, doctor: Doctor, patient: Patient, drug: Drug, diagnosis: str) -> Prescription:
        p = Prescription(self._next_prescription_id, doctor, patient, drug, diagnosis)
        if patient.has_intangible:
            p.is_intangible = True
        self.prescriptions.append(p)
        self._next_prescription_id += 1
        return p