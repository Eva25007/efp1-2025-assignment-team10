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
        ## Start of Doctor Menu (USE CASE ΚΑΤΑΧΩΡΗΣΗ ΝΕΑΣ ΣΥΝΤΑΓΗΣ)
        if role == "1":
            license_id = input("[For testing (licence100, licence200)] \n Παρακαλώ εισάγετε ID Ιατρού: ")
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
                    amka = input("[For testing (amka100: ασθενής με άυλη, amka200:ασθενής χωρίς άυλη)] \n Παρακαλώ εισάγετε ΑΜΚΑ Ασθενούς: ")
                    patient = system.find_patient(amka)
                    if not patient: 
                        print("Ο ασθενής δεν βρέθηκε.")
                        continue
                    
                    drugs = []
                    while True:
                        barcode = input("[For testing (DRUG001, DRUG002, DRUG003)] \n Παρακαλώ εισάγετε Barcode Φαρμάκου (ή '0' για ολοκλήρωση επιλογής φαρμάκων): ")
                        if barcode == '0':
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
                        print("(Στάλθηκε SMS καθώς ο ασθενής διαθέτει την υπηρεσία 'Άυλη Συνταγογράφηση')")
                    else:
                        print("(Εκτύπωση καθώς ο ασθενής δεν διαθέτει την υπηρεσία 'Άυλη Συνταγογράφηση')")

                elif sub_choice == "0":
                    break
        ## End of Doctor Menu
        
        # Start of Pharmacist Menu (USE CASE ΕΚΤΕΛΕΣΗ ΣΥΝΤΑΓΗΣ)
        elif role == "2":
            license_id = input("[For testing (pharm100, pharm200)] \n Παρακαλώ εισάγετε Αριθμό Άδειας Φαρμακείου:  ")
            pharmacist = system.find_pharmacist(license_id)
            if not pharmacist:
                print("Λάθος άδεια φαρμακείου.")
                continue
            
            while True:
                print(f"\n=== ΜΕΝΟΥ ΦΑΡΜΑΚΟΠΟΙΟΥ ===")
                print(f"Φαρμακοποιός: {pharmacist.surname} {pharmacist.name}")
                print(f"Φαρμακείο: {pharmacist.pharmacy_address}")
                print("-" * 40)
                print("1. Εκτέλεση Συνταγής")
                print("0. Πίσω")
                
                sub_choice = input("Επιλογή: ")

                if sub_choice == "1":
                    # --- ΕΚΤΕΛΕΣΗ ΣΥΝΤΑΓΗΣ ---
                    print("\n" + "="*50)
                    print(" ΕΚΤΕΛΕΣΗ ΣΥΝΤΑΓΗΣ ")
                    print("="*50)
                    
                    # Επιλογή τρόπου σάρωσης
                    print("\nΤρόπος σάρωσης:")
                    print("[For testing (demo100: συνταγή ασθενούς με άυλη, demo200: συνταγή ασθενούς με εκτύπωση)]")
                    print("1. Σάρωση από χαρτί (εκτύπωση)")
                    print("2. Σάρωση από κινητό (άυλη)")
                    scan_type = input("Επιλογή: ")
                    
                    if scan_type == "2":
                        print("\n  Ο ασθενής πρέπει να εμφανίσει το barcode στο κινητό του")
                        print("Σαρώστε το barcode από την οθόνη του κινητού")
                    
                    prescription_barcode = input("\nΣάρωση barcode συνταγής (εκτύπωση): ")
                    
                    prescription = system.find_prescription(prescription_barcode)
                    if not prescription:
                        print(" Η συνταγή δεν βρέθηκε!")
                        continue

                    if prescription.is_executed:
                        print(f" [!] Η συνταγή εκτελέστηκε ήδη στις {prescription.execution_date}")
                        continue
                    
                    # Έλεγχος αν είναι άυλη
                    if prescription.is_intangible and scan_type == "1":
                        print("  Προσοχή: Αυτή είναι άυλη συνταγή!")
                        print("Πρέπει να σαρωθεί από το κινητό του ασθενούς")
                        continue
                    
                    while not prescription.is_executed:
                        print("\n" + "="*40)
                        print(f" ΦΑΡΜΑΚΑ ΣΥΝΤΑΓΗΣ #{prescription.prescription_id}")
                        print("-" * 40)
                        
                        for i, drug in enumerate(prescription.drugs, 1):
                            if drug.barcode in prescription.scanned_drugs:
                                status = "ΕΠΑΛΗΘΕΥΤΗΚΕ [✓]"
                            else:
                                status = "ΕΚΚΡΕΜΕΙ [X]"
                        
                            print(f"{i}. {drug.name:<15} | Barcode: {drug.barcode:<8} | {status}")
                        
                        print("-" * 40)
                        
                        # Αν όλα τα φάρμακα της συνταγής έχουν σαρωθεί
                        if len(prescription.scanned_drugs) == len(prescription.drugs):
                            print("\n[!] ΟΛΑ ΤΑ ΦΑΡΜΑΚΑ ΕΠΑΛΗΘΕΥΤΗΚΑΝ")
                            confirm = input("Πληκτρολογήστε '1' για εκτέλεση ή '0' για ακύρωση: ")
                            if confirm == '1':
                                if system.execute(pharmacist.pharmacy_license_id, prescription):
                                    print(f"\n✓ Η συνταγή εκτελέστηκε επιτυχώς στις {prescription.execution_time}!")
                                    break
                            else:
                                break

                        drug_barcode = input("Σάρωση (πληκτρολόγηση) barcode φαρμάκου (ή '0' για έξοδο): ")
                        if drug_barcode == '0': break
                        
                        result = system.scan_drug_for_prescription(drug_barcode, prescription)
                        
                        if result == "scanned":
                            print(" [+] Επιτυχής επαλήθευση.")
                        elif result == "already_scanned":
                            print(" [!] Το φάρμακο έχει ήδη σαρωθεί.")
                        else:
                            print(" [X] ΛΑΘΟΣ ΦΑΡΜΑΚΟ: Δεν ανήκει στη συνταγή.")

                elif sub_choice == "0":
                    break

        ## λούπ φαρμακοποιού κλείσιμο
        elif role == "0":
            print("Αντίο!")
            break

        ##λούπ κεντρικού μενού κλείσιμο
        else:
            print("Μη έγκυρη επιλογή.")
        ## End Main Menu

if __name__ == "__main__":
    main()