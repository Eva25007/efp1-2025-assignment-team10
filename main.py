from services import Digital_Prescription
from datetime import datetime  ### ΕΠΑΛΗΘΕΥΣΗ: ΠΡΟΣΘΗΚΗ ΕΙΣΑΓΩΓΗΣ

def main():
    system = Digital_Prescription()
    ## Start Main Menu
    print("=== Σύστημα Ηλεκτρονικής Συνταγογράφησης ===")

    while True:
        print("\n=== ΚΕΝΤΡΙΚΟ ΜΕΝΟΥ ===")
        print("1. Ιατρός (Συνταγογράφηση)")
        print("2. Φαρμακοποιός (Εκτέλεση Συνταγής)")
        print("0. Έξοδος")
        
        role = input("Επιλέξτε ρόλο: ")
        ## Start of Doctor Menu
        if role == "1":
            license_id = input("ID Ιατρού: hint (licence100, licence200, licence300)")
            doctor = system.find_doctor(license_id)
            if not doctor:
                print("Λάθος ID.")
                continue
            
            while True:
                print(f"\n--- Menu Ιατρού ---\n Καλωσήρθες, Dr. {doctor.surname} {doctor.name}!")
                print("1. Νέα Συνταγή")
                print("0. Πίσω")
                sub_choice = input("Επιλογή: ")

                if sub_choice == "1":
                    amka = input("ΑΜΚΑ Ασθενούς: hint (amka100, amka200, amka300)")
                    patient = system.find_patient(amka)
                    if not patient: 
                        print("Ο ασθενής δεν βρέθηκε.")
                        continue
                    
                    drugs = []
                    while True:
                        barcode = input("Barcode Φαρμάκου (ή 'τέλος' για ολοκλήρωση): ")
                        if barcode.lower() == 'τέλος':
                            break
                        
                        drug = system.find_drug(barcode)
                        if not drug:
                            print("Το φάρμακο δεν βρέθηκε.")
                            continue
                        
                        drugs.append(drug)
                        print(f"Προστέθηκε: {drug.name}")
                    
                    if not drugs:
                        print("Πρέπει να προσθέσετε τουλάχιστον ένα φάρμακο.")
                        continue
						
                    
                    diagnosis = input("Διάγνωση: ")
                    presc = system.create_prescription(doctor, patient, drugs, diagnosis)
                    print(f"\n✓ Επιτυχία! Δημιουργήθηκε Συνταγή")
                    print(f"  ID Συνταγής: {presc.prescription_id}")
                    print(f"  Barcode: {presc.barcode}")
                    print(f"  Ασθενής: {patient.surname} {patient.name}")
                    print(f"  Πλήθος φαρμάκων: {len(drugs)}")
                    if presc.is_intangible:
                        print("(Στάλθηκε SMS λόγω Άυλης)")
                    else:
                        print("(Εκτύπωση σε χαρτί)")

                elif sub_choice == "0":
                    break
        ## End of Doctor Menu
        
       

       
    
        elif role == "0":
            print("Αντίο!")
            break
        else:
            print("Μη έγκυρη επιλογή.")
        ## End Main Menu

if __name__ == "__main__":
    main()