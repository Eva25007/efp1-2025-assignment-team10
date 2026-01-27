from services import Digital_Prescription

def main():
    system = Digital_Prescription()
    ## Start Main Menu
    print("=== Σύστημα Ηλεκτρονικής Συνταγογράφησης ===")

    while True:
        print("\n=== ΚΕΝΤΡΙΚΟ ΜΕΝΟΥ ===")
        print("1. Ιατρός (Συνταγογράφηση)")
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
                    
                    barcode = input("Barcode Φαρμάκου: ")
                    drug = system.find_drug(barcode)
                    if not drug:
                        print("Το φάρμακο δεν βρέθηκε.")
                        continue
                    
                    diagnosis = input("Διάγνωση: ")
                    presc = system.create_prescription(doctor, patient, drug, diagnosis)
                    print(f"Επιτυχία! ID Συνταγής: {presc.prescription_id}")
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