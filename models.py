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