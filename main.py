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
        
        # Start of Pharmacist Menu (USE CASE ΕΚΤΕΛΕΣΗ ΣΥΝΤΑΓΗΣ)
        elif role == "2":
            license_id = input("Αριθμός Άδειας Φαρμακείου: hint (pharm100, pharm200, pharm300): ")
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
                    print(" ΕΠΑΛΗΘΕΥΣΗ ΦΑΡΜΑΚΟΥ")
                    print("="*50)
                    
                    # Επιλογή τρόπου σάρωσης
                    print("\nΤρόπος σάρωσης:")
                    print("1. Σάρωση από χαρτί (εκτύπωση)")
                    print("2. Σάρωση από κινητό (άυλη)")
                    scan_type = input("Επιλογή: ")
                    
                    if scan_type == "2":
                        print("\n  Ο ασθενής πρέπει να εμφανίσει το barcode στο κινητό του")
                        print("Σαρώστε το barcode από την οθόνη του κινητού")
                    
                    prescription_barcode = input("\nΣάρωση barcode συνταγής: ")
                    
                    prescription = system.find_prescription(prescription_barcode)
                    if not prescription:
                        print(" Η συνταγή δεν βρέθηκε!")
                        continue
                    
                    # Έλεγχος αν είναι άυλη
                    if prescription.is_intangible and scan_type == "1":
                        print("  Προσοχή: Αυτή είναι άυλη συνταγή!")
                        print("Πρέπει να σαρωθεί από το κινητό του ασθενούς")
                        continue
                    
                    # Εμφάνιση λίστας
                    print(f"\n Συνταγή #{prescription.prescription_id}")
                    print(f" Ασθενής: {prescription.patient.surname} {prescription.patient.name}")
                    print(f" ΑΜΚΑ: {prescription.patient.amka}")
                    print(f" Διάγνωση: {prescription.diagnosis}")
                    print("-" * 50)
                    
                    # Αρχικοποίηση λίστας επαλήθευσης
                    verification_list = []
                    for drug in prescription.drugs:
                        verification_list.append({
                            'drug': drug,
                            'verified': False,
                            'timestamp': None
                        })
                    
                    # Κυρίως βρόχος επαλήθευσης
                    while True:
                        print("\n" + "="*50)
                        print(" ΛΙΣΤΑ ΦΑΡΜΑΚΩΝ ΓΙΑ ΕΠΑΛΗΘΕΥΣΗ")
                        print("="*50)
                        print(f"{'No':<3} {'Barcode':<12} {'Ονομασία':<20} {'Κατάσταση':<15}")
                        print("-"*50)
                        
                        for i, item in enumerate(verification_list, 1):
                            status = " ΕΠΑΛΗΘΕΥΜΕΝΟ" if item['verified'] else " ΕΚΚΡΕΜΕΙ"
                            print(f"{i:<3} {item['drug'].barcode:<12} {item['drug'].name:<20} {status:<15}")
                        
                        print("-"*50)
                        
                        # Έλεγχος αν όλα έχουν επαληθευτεί
                        all_verified = all(item['verified'] for item in verification_list)
                        if all_verified:
                            print("\n ΟΛΑ ΤΑ ΦΑΡΜΑΚΑ ΕΠΑΛΗΘΕΥΤΗΚΑΝ!")
                            print(f" Ημερομηνία: {datetime.now().strftime('%Y-%m-%d')}")
                            print(f" Ώρα: {datetime.now().strftime('%H:%M:%S')}")
                            break
                        
                        # Σάρωση επόμενου φαρμάκου
                        print(f"\nΕπανάληψη: {sum(1 for item in verification_list if item['verified'])}/{len(verification_list)}")
                        drug_barcode = input("Σάρωση barcode φαρμάκου (ή 'q' για έξοδο): ")
                        
                        if drug_barcode.lower() == 'q':
                            print(" Έξοδος από επαλήθευση")
                            break
                        
                        # Αναζήτηση φαρμάκου στη λίστα
                        found = False
                        for item in verification_list:
                            if item['drug'].barcode == drug_barcode:
                                found = True
                                if item['verified']:
                                    print("  Αυτό το φάρμακο έχει ήδη επαληθευτεί")
                                else:
                                    item['verified'] = True
                                    item['timestamp'] = datetime.now().strftime('%H:%M:%S')
                                    print(f" ΕΠΙΤΥΧΗΣ ΕΠΑΛΗΘΕΥΣΗ: {item['drug'].name}")
                                break
                        
                        if not found:
                            print(" ΛΑΘΟΣ ΦΑΡΜΑΚΟ / ΜΗ ΕΓΚΥΡΟ")
                            print("Παρακαλώ σαρώστε το σωστό φάρμακο από τη λίστα")
                        
					# Σάρωση φαρμάκων
                    scanned_drugs = []
                    while len(scanned_drugs) < len(prescription.drugs):
                        print(f"\nΣαρώθηκαν {len(scanned_drugs)}/{len(prescription.drugs)} φάρμακα")
                        drug_barcode = input("Σάρωση barcode φαρμάκου (ή 'q' για έξοδο): ")
                        
                        if drug_barcode.lower() == 'q':
                            break
                        
                        # Έλεγχος αν το φάρμακο ανήκει στη συνταγή
                        result = prescription.scan_drug(drug_barcode)
                        if result == "already_scanned":
                            print("  Αυτό το φάρμακο έχει ήδη σαρωθεί.")
                        elif result == "not_found":
                            print(" Το φάρμακο δεν ανήκει σε αυτή τη συνταγή.")
                        elif result == "scanned":
                            print(" Σαρώθηκε επιτυχώς!")
                            scanned_drugs.append(drug_barcode)
                            
                            # Ενημέρωση εμφάνισης
                            print("\nΕνημερωμένη λίστα:")
                            for i, drug in enumerate(prescription.drugs, 1):
                                status = "Approved" if drug.barcode in prescription.scanned_drugs else "Λάθος Φάρμακο"
                                print(f"{i}. {drug.name} {status}")

                    # Αν όλα τα φάρμακα σαρώθηκαν
                    if len(scanned_drugs) == len(prescription.drugs):
                        print(f"\n{'='*50}")
                        print("Όλα τα φάρμακα σαρώθηκαν!")
                        
                        # Επιβεβαίωση εκτέλεσης
                        confirm = input("Επιλέξτε 'εκτέλεση' για ολοκλήρωση: ")
                        if confirm.lower() == 'εκτέλεση':
                            # Εκτέλεση συνταγής
                            success = prescription.execute(pharmacist.pharmacy_license_id)
                            if success:
                                print(f"\n{'✓'*50}")
                                print("✓ Η συνταγή εκτελέστηκε επιτυχώς!")
                                print(f"  Ημερομηνία: {prescription.execution_date}")
                                print(f"  Ώρα: {prescription.execution_time}")
                                print(f"  Φαρμακοποιός: {pharmacist.surname} {pharmacist.name}")
                                print(f"  Άδεια Φαρμακείου: {pharmacist.pharmacy_license_id}")
                                print(f"{'✓'*50}")
                            else:
                                print("Η εκτέλεση απέτυχε.")
                    else:
                        print(" Δεν σαρώθηκαν όλα τα φάρμακα. Η διαδικασία ακυρώθηκε.")
    
        elif role == "0":
            print("Αντίο!")
            break
        else:
            print("Μη έγκυρη επιλογή.")
        ## End Main Menu

if __name__ == "__main__":
    main()