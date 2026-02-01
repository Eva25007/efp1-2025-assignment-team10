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
        
        if doctor1 and patient1 and all(drugs1):
            self.create_prescription(doctor1, patient1, drugs1, "Βρογχοπνευμονία")

        doctor2 = self.find_doctor("licence200")
        patient2 = self.find_patient("amka200")
        drugs2 = [self.find_drug("DRUG002")]
        
        if doctor2 and patient2 and all(drugs2):
            self.create_prescription(doctor2, patient2, drugs2, "Πυρετός")

        
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
    def scan_drug(self, drug_barcode: str) -> str:
        """Σάρωση φαρμάκου και επιστροφή status"""
        # Έλεγχος αν το φάρμακο είναι στη συνταγή
        drug_found = None
        for drug in self.drugs:
            if drug.barcode == drug_barcode:
                drug_found = drug
                break
        
        if not drug_found:
            return "not_found"
        
        # Έλεγχος αν έχει ήδη σαρωθεί
        if drug_barcode in self.scanned_drugs:
            return "already_scanned"
        
        # Προσθήκη στη λίστα σαρωμένων
        self.scanned_drugs.append(drug_barcode)
        return "scanned"
    
    ### ΕΠΑΛΗΘΕΥΣΗ: ΜΕΘΟΔΟΣ ΓΙΑ ΕΠΑΛΗΘΕΥΣΗ ΦΑΡΜΑΚΟΥ
    def verify_drug(self, drug_barcode: str) -> tuple[bool, str]:
        """
        Επαληθεύει αν το φάρμακο ανήκει στη συνταγή.
        Επιστρέφει (success, message)
        """
        # Έλεγχος αν το φάρμακο είναι στη συνταγή
        drug_found = None
        for drug in self.drugs:
            if drug.barcode == drug_barcode:
                drug_found = drug
                break
        
        if not drug_found:
            return False, "Λάθος Φάρμακο / Μη έγκυρο"
        
        # Έλεγχος αν έχει ήδη σαρωθεί
        if drug_barcode in self.scanned_drugs:
            return True, "Το φάρμακο έχει ήδη επαληθευτεί"
        
        # Προσθήκη στη λίστα σαρωμένων
        self.scanned_drugs.append(drug_barcode)
        return True, "Επιτυχής επαλήθευση"
    ### ΤΕΛΟΣ ΕΠΑΛΗΘΕΥΣΗΣ

    def execute(self, pharmacy_license_id: str) -> bool:
        """Εκτέλεση συνταγής αν όλα τα φάρμακα έχουν σαρωθεί"""
        if len(self.scanned_drugs) == len(self.drugs):
            from datetime import datetime
            now = datetime.now()
            self.execution_date = now.strftime("%Y-%m-%d")
            self.execution_time = now.strftime("%H:%M:%S")
            self.executed_by = pharmacy_license_id
            self.is_executed = True
            return True
        return False

    def __str__(self):
        status = "ΕΚΤΕΛΕΣΜΕΝΗ" if self.is_executed else "ΕΚΚΡΕΜΕΙ"
        return f"Συνταγή #{self.prescription_id} - Ασθενής: {self.patient.surname} - Κατάσταση: {status}"