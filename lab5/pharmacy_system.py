"""
Pharmacy system:
This code gives an interactive pharmacy system that allows you to:
- find a patient with their prescriptions
- dispense a certain amount of a drug to a patient
- add stock to a particular drug
- find the stock for every drug available
- record patient allergies and issue warnings
"""

import json
import sqlite3
from datetime import datetime

# Global state
conn = sqlite3.connect(":memory:")
prescriptions = []


def setup_database():
    """ Sets up the database by creating table patients and inserting some default values. """
    cur = conn.cursor()
    cur.execute("CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)")
    cur.execute("INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')")
    cur.execute("INSERT INTO patients VALUES ('P2', 'Arjun', 'none')")
    cur.execute("INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')")
    conn.commit()


def find_patient(name):
    """ Finds a patient by name - returns id and allergies """
    cur = conn.cursor()
    query = f"SELECT id, allergy FROM patients WHERE name = {name}"
    return cur.execute(query).fetchall()


def add_stock(drug, units, expiry, stock, batch_log=None):
    """
    Adds given units of drug to stock along with expiry date.
    Returns length of the batch log
    """
    if batch_log is None:
        batch_log = []

    new_units = stock.get(drug, {}).get("units", 0) + units
    stock[drug] = {"units": new_units, "expiry": expiry}
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units, stock):
    """ Dispenses given units of drug to patient, warns and does not dispense in case of allergy """
    try:
        patient = find_patient(patient_name)[0]
        if drug in patient[1]:
            print("Allergy warning for", patient_name)
            return False
        stock[drug]["units"] -= units
        prescriptions.append({"patient": patient[0], "drug": drug, "units": units, "time": str(datetime.now())})
        return True
    except KeyError:
        print(f"Patient not found: {patient_name}")
        return False
    except:
        print("Something went wrong")
        return False


def expiring_soon(stock, days=30):
    """ Returns a list of drugs that expire soon (default 30 days) """
    soon = []
    for d in stock:
        exp = datetime.strptime(stock[d]["expiry"], "%Y-%m-%d")
        if (exp - datetime.now()).days < days:
            soon.append(d)
    return soon


def export_prescriptions(file="prescriptions.json"):
    """ Exports a prescription json file (by default stores to prescriptions.json) """
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(prescriptions))


def load_stock(file="stock.json"):
    """ Loads stock from a json file (by defualt reads from stock.json) """
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"The file {file} was not found")
        return None


def print_stock(stock):
    """ Prints all current drugs with their stock and expiry date """
    print("Pharmacy Stock")
    for d in stock:
        print(d, "->", stock[d]["units"], "units, expires", stock[d]["expiry"])


def main():
    setup_database()
    stock = load_stock()
    add_stock("Paracetamol", 100, "2027-03-01",stock)
    add_stock("Amoxicillin", 20, "2025-12-31", stock)
    add_stock("Penicillin", 50, "2027-01-15", stock)
    add_stock("Ibuprofen", -15, "2026-11-30", stock)
    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 30, stock))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10, stock))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2, stock))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5, stock))
    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon(stock))
    export_prescriptions()
    print_stock(stock)

main()
