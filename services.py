from models import Doctor, Patient, Pharmacist, Drug, Prescription

class Digital_Prescription:
    def __init__(self):
        self.doctors: list[Doctor] = []
        self.prescriptions: list[Prescription] = []
        self.patients: list[Patient] = []
        self.pharmacists: list[Pharmacist] = []
        self.drugs: list[Drug] = []

        self._next_prescription_id = 1
        self._seed_demo_data()

    def _seed_demo_data(self) -> None:
        # Doctors
        self.doctors.append(Doctor("Nick", "Gkizis", "nickG", "Pathologist", "licence100"))
        self.doctors.append(Doctor("Joanah", "Pavlou", "joanahP", "Cardiologist", "licence200"))
        self.doctors.append(Doctor("Bruce", "Dickinson", "bruceD", "ENT", "licence300"))

		 # Pharmacists
        self.pharmacists.append(Pharmacist("John", "Smith", "johnS", "Πατησίων 123, Αθήνα", "pharm100"))
        self.pharmacists.append(Pharmacist("Mary", "Johnson", "maryJ", "Εγνατίας 45, Θεσσαλονίκη", "pharm200"))
        self.pharmacists.append(Pharmacist("George", "Papadopoulos", "geoP", "Κορίνθου 67, Πάτρα", "pharm300"))

        # Patients
        self.patients.append(Patient("Pavlina", "Ioannou", "pavlinaIoannou", "amka100", True, "Athens", "6900000000", "EFKA"))
        self.patients.append(Patient("George", "Konstantinou", "georgeKonstantinou", "amka200", False, "Thessaloniki", "6911111111", "IKA"))
        self.patients.append(Patient("Maria", "Papadopoulou", "mariaPapadopoulou", "amka300", True, "Patra", "6922222222", "OGA"))
        
		# Drugs
        self.drugs.append(Drug("Amoxicillin", "DRUG001", 8.50, "Αμοξικιλλίνη", "Δισκία 500mg"))
        self.drugs.append(Drug("Ibuprofen", "DRUG002", 5.20, "Ιβουπροφαίνη", "Δισκία 200mg"))
        self.drugs.append(Drug("Paracetamol", "DRUG003", 3.80, "Παρακεταμόλη", "Δισκία 500mg"))
        self.drugs.append(Drug("Ventolin", "DRUG004", 12.30, "Σαλβουταμόλη", "Ατμός"))
        self.drugs.append(Drug("Lasix", "DRUG005", 7.90, "Φουροσεμίδη", "Δισκία 40mg"))
		
		 # Create some sample prescriptions
        doctor1 = self.find_doctor("licence100")
        patient1 = self.find_patient("amka100")
        drugs1 = [self.find_drug("DRUG001"), self.find_drug("DRUG003")]
        
        doctor2 = self.find_doctor("licence200")
        patient2 = self.find_patient("amka200")
        drugs2 = [self.find_drug("DRUG002")]

        dummy_presc = self.create_prescription(doctor1, patient1, drugs1, "Βρογχοπνευμονία")
        dummy_presc.barcode = "demo100"

        dummy_presc = self.create_prescription(doctor2, patient2, drugs2, "Πονοκέφαλος")
        dummy_presc.barcode = "demo200"
        
    # General Functions

    def find_doctor(self, license_id: str) -> Doctor | None:
        return next((d for d in self.doctors if d.medical_license_id == license_id), None)

    def find_drug(self, barcode: str) -> Drug | None:
        return next((d for d in self.drugs if d.barcode == barcode), None)

    def find_patient(self, amka: str) -> Patient | None:
        return next((p for p in self.patients if p.amka == amka), None)
    	
    def find_pharmacist(self, license_id: str) -> Pharmacist | None:
        return next((p for p in self.pharmacists if p.pharmacy_license_id == license_id), None)

    def find_prescription(self, barcode: str) -> Prescription | None:
        return next((p for p in self.prescriptions if p.barcode == barcode), None)

    #Functions Ιατρού

    def create_prescription(self, doctor: Doctor, patient: Patient, drugs: list, diagnosis: str) -> Prescription:
        p = Prescription(self._next_prescription_id, doctor, patient, drugs, diagnosis)
        if patient.has_intangible_perscription:
            p.is_intangible = True
        self.prescriptions.append(p)
        self._next_prescription_id += 1
        return p
    
    #Functions Φαρμακοποιού

    def scan_drug_for_prescription(self, drug_barcode, prescription):
        return prescription.scan_drug(drug_barcode)

    def execute(self, pharmacy_license_id, prescription):
        return prescription.execute(pharmacy_license_id)

    def __str__(self):
        status = "ΕΚΤΕΛΕΣΜΕΝΗ" if self.is_executed else "ΕΚΚΡΕΜΕΙ"
        return f"Συνταγή #{self.prescription_id} - Ασθενής: {self.patient.surname} - Κατάσταση: {status}"