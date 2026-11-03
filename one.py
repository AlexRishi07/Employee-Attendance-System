#Name = Rishi Kumar
#email = rishi.kumar@rungta.org
#section = B2
#erp = RU-26-02614
#PS no. = 14

"""Employee Attendance System
Console-based employee attendance manager with file persistence.
"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "attendance.txt"
FIRST_EMPLOYEE_NUMBER = 101
VALID_STATUSES = {"P": "Present", "A": "Absent", "L": "Leave"}


def load_data():
    """Load employee dictionaries from the data file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            print("Warning: attendance.txt has an invalid format. Starting with empty records.")
            return []

        employees = []
        for item in data:
            if not isinstance(item, dict):
                continue
            employee_id = item.get("id")
            name = item.get("name")
            records = item.get("records", {})
            if isinstance(employee_id, str) and isinstance(name, str) and isinstance(records, dict):
                employees.append({"id": employee_id, "name": name, "records": records})
        return employees
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read attendance.txt. Starting with empty records.")
        return []


def save_data(employees):
    """Save all employee records after every successful change."""
    temporary_file = DATA_FILE.with_suffix(DATA_FILE.suffix + ".tmp")
    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)
    os.replace(temporary_file, DATA_FILE)


def find_employee(employees, employee_id):
    """Return the employee dictionary, or None if the ID does not exist."""
    for employee in employees:
        if employee["id"].upper() == employee_id.strip().upper():
            return employee
    return None


def next_employee_id(employees):
    """Generate sequential IDs beginning at E101."""
    numbers = []
    for employee in employees:
        employee_id = employee.get("id", "")
        if isinstance(employee_id, str) and employee_id.startswith("E"):
            try:
                numbers.append(int(employee_id[1:]))
            except ValueError:
                pass
    next_number = max(numbers, default=FIRST_EMPLOYEE_NUMBER - 1) + 1
    return f"E{next_number}"


def add_employee(employees):
    """Add a new employee and persist the change."""
    name = input("Enter employee name: ").strip()
    if not name:
        print("Invalid name. Employee name cannot be empty.")
        return

    employee_id = next_employee_id(employees)
    employees.append({"id": employee_id, "name": name, "records": {}})
    save_data(employees)
    print(f"Employee added: {employee_id} | {name}")


def valid_date(date_text):
    """Check that a date is a real calendar date in YYYY-MM-DD format."""
    try:
        parsed = datetime.strptime(date_text, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d") == date_text
    except ValueError:
        return False


def mark_attendance(employees):
    """Mark P/A/L attendance after validating employee, date and status."""
    employee_id = input("Enter employee ID: ").strip().upper()
    employee = find_employee(employees, employee_id)
    if employee is None:
        print(f"Employee {employee_id} not found.")
        return

    date_text = input("Enter date (YYYY-MM-DD): ").strip()
    if not valid_date(date_text):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    status = input("Enter status (P=Present, A=Absent, L=Leave): ").strip().upper()
    if status not in VALID_STATUSES:
        print("Invalid status. Enter P, A or L.")
        return

    if date_text in employee["records"]:
        print(f"Attendance for {date_text} is already marked.")
        return

    employee["records"][date_text] = status
    save_data(employees)
    print(f"Attendance marked: {employee['id']} | {employee['name']} | {date_text} | {VALID_STATUSES[status]}")


def show_report(employees):
    """Display the attendance summary and attendance percentage."""
    employee_id = input("Enter employee ID: ").strip().upper()
    employee = find_employee(employees, employee_id)
    if employee is None:
        print(f"Employee {employee_id} not found.")
        return

    records = employee["records"]
    present = sum(1 for status in records.values() if status == "P")
    absent = sum(1 for status in records.values() if status == "A")
    leave = sum(1 for status in records.values() if status == "L")
    marked_days = present + absent + leave
    percentage = (present / marked_days * 100) if marked_days else 0.0

    print(f"{employee['name']}: Present{present} | Absent{absent} | Leave{leave}")
    if marked_days == 0:
        print(f"Attendance: {percentage:.2f}% (no records)")
    else:
        print(f"Attendance: {percentage:.2f}%")


def display_menu():
    """Print the available attendance-system actions."""
    print("\n===== Employee Attendance System =====")
    print("1. Add Employee")
    print("2. Mark Attendance")
    print("3. View Attendance Report")
    print("4. Exit")


def main():
    """Load employee data and run the attendance-system menu loop."""
    employees = load_data()
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            mark_attendance(employees)
        elif choice == "3":
            show_report(employees)
        elif choice == "4":
            print("Thank you for using Employee Attendance System.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
