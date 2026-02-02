import uuid

class User: # USER (υπερκλάση / super) από εδώ κληρονομούν Ιατρός, Φαρμακοποιός και Ασθενής
    def __init__(self, name: str, 
                 surname: str, 
                 username: str):
        self.name = name
        self.surname = surname
        self.username = username

    def __str__(self) -> str:
        return f"{self.surname} {self.name}"

class Doctor(User): # ΙΑΤΡΟΣ
    def __init__(self, name: str,
                 surname: str, 
                 username: str, 
                 specialty: str, 
                 medical_license_id: str):
        super().__init__(name, surname, username)
        self.specialty = specialty
        self.medical_license_id = medical_license_id

    def __str__(self) -> str:
        return f"""Καλησπέρα σας: {self.surname} {self.name} 
        \n [Ειδικότητα: {self.specialty}]
        \n [Αριθμός Ιατρικής Άδειας: {self.medical_license_id}]"""

class Pharmacist(User): # ΦΑΡΜΑΚΟΠΟΙΟΣ
    def __init__(self, name: str,
                 surname: str, 
                 username: str, 
                 pharmacy_address: str, 
                 pharmacy_license_id: str):
        super().__init__(name, surname, username)
        self.pharmacy_address = pharmacy_address
        self.pharmacy_license_id = pharmacy_license_id

    def __str__(self) -> str:
        return f"""Καλησπέρα σας: {self.surname} {self.name} 
        \n [Διεύθυνση Φαρμακείου: {self.pharmacy_address}] 
        \n [Αριθμός Άδειας Φαρμακείου: {self.pharmacy_license_id}]"""

class Patient(User): # AΣΘΕΝΗΣ
    def __init__(self, name: str, 
                 surname: str,  
                 username: str, 
                 amka: str, 
                 has_intangible_perscription: bool, 
                 address: str, 
                 phone_number: str, 
                 insurance_provider: str):
        super().__init__(name, surname, username)
        self.amka = amka
        self.has_intangible_perscription = has_intangible_perscription
        self.address = address
        self.phone_number = phone_number
        self.insurance_provider = insurance_provider

    def __str__(self) -> str:
        return f"""Καλησπέρα σας: {self.surname} {self.name}
        \n [AMKA: {self.amka}] 
        \n [Διεύθυνση: {self.address}]
        \n [Τηλέφωνο: {self.phone_number}]
        \n [Ασφαλιστικός Φορέας: {self.insurance_provider}]"""
		
class Drug:
    def __init__(self, name: str, barcode: str, price: float, active_substance: str = "", form: str = ""):
        self.name = name
        self.barcode = barcode
        self.price = price
        self.active_substance = active_substance
        self.form = form

    def __str__(self):
        return f"{self.name} ({self.barcode}) - {self.price}€"

class Prescription:
    def __init__(self, prescription_id: int, doctor: Doctor, patient: Patient, drugs: list, diagnosis: str):
        self.prescription_id = prescription_id
        self.barcode = str(uuid.uuid4())[:8]  # Βάζουμε barcode για τη συνταγή
        self.doctor = doctor
        self.patient = patient
        self.drugs = drugs  # Λίστα από Drug αντικείμενα
        self.diagnosis = diagnosis
        self.is_intangible = patient.has_intangible_perscription
        self.scanned_drugs = []  # Λίστα για τα φάρμακα που έχουν σαρωθεί
        self.execution_date = None
        self.execution_time = None
        self.executed_by = None  # Άδεια φαρμακείου που εκτέλεσε
        self.is_executed = False

    def scan_drug(self, drug_barcode: str) -> str:
        """Σάρωση φαρμάκου και επιστροφή status"""
        # Έλεγχος αν το φάρμακο είναι στη συνταγή
        drug_found = next((d for d in self.drugs if d.barcode == drug_barcode), None)
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
