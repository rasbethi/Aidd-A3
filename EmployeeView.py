# EmployeeView.py

def show_menu():
    print("\nEmployee Management System")
    print("1. Create New Employee")
    print("2. Edit Existing Employee")
    print("3. Delete Existing Employee")
    print("4. Display Employees")
    print("5. Quit")

def prompt_employee_data(is_manager=False):
    emp_id = input("Employee ID: ").strip()
    fname = input("First Name: ").strip()
    lname = input("Last Name: ").strip()
    department = input("Department (3 letters, e.g., FIN): ").strip()
    phone = input("Phone (any format, 10 digits): ").strip()
    if is_manager:
        team_size = input("Team Size (integer): ").strip()
        return emp_id, fname, lname, department, phone, team_size
    return emp_id, fname, lname, department, phone

def prompt_edit_field(label, current):
    return input(f"{label} [{current}] (Enter to keep): ")

def show_employees(employees):
    if not employees:
        print("No employees found.")
        return

    headers = ["No.", "Emp ID", "Name", "Department", "Phone", "Role", "Team Size"]
    rows = []

    for idx, emp in enumerate(employees, start=1):
        role = "Manager" if hasattr(emp, "team_size") else "Employee"
        team_size = emp.team_size if role == "Manager" else ""
        rows.append([
            str(idx),
            str(emp.id),
            f"{emp.fname} {emp.lname}",
            emp.department,
            emp.phNumber,
            role,
            str(team_size)
        ])

    # calculate column widths
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]

    # header
    header = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    separator = "  ".join("-" * w for w in col_widths)

    print(header)
    print(separator)

    # rows
    for row in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(row, col_widths)))



def show_message(msg):
    print(msg)
