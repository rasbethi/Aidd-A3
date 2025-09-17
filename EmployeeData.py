# EmployeeData.py
import csv
import os
from employee import Employee, Manager

CSV_FILE = "employee_data.csv"

def load_employees():
    """Load employees from CSV; returns a list of Employee/Manager objects."""
    employees = []
    if not os.path.exists(CSV_FILE):
        return employees

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_type = (row.get("type") or "Employee").strip()
            if emp_type == "Manager":
                # team_size might be stored as string; Manager setter will validate/convert
                team_size = row.get("team_size", "").strip()
                emp = Manager(
                    row["id"], row["fname"], row["lname"],
                    row["department"], row["phNumber"], team_size
                )
            else:
                emp = Employee(
                    row["id"], row["fname"], row["lname"],
                    row["department"], row["phNumber"]
                )
            employees.append(emp)
    return employees


def save_employees(employees):
    """Save employees list to CSV (overwrites file each time)."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "fname", "lname", "department", "phNumber", "type", "team_size"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            if isinstance(emp, Manager):
                writer.writerow({
                    "id": emp.id,
                    "fname": emp.fname,
                    "lname": emp.lname,
                    "department": emp.department,
                    "phNumber": emp.getphNumber(),
                    "type": "Manager",
                    "team_size": emp.team_size
                })
            else:
                writer.writerow({
                    "id": emp.id,
                    "fname": emp.fname,
                    "lname": emp.lname,
                    "department": emp.department,
                    "phNumber": emp.getphNumber(),
                    "type": "Employee",
                    "team_size": ""
                })
