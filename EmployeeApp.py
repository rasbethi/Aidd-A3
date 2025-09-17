from employee import Employee, Manager
import EmployeeData
import EmployeeView

# --- Validators ---
def validate_fname(val):
    if not val.isalpha():
        raise ValueError("First name must contain only letters.")
    return val

def validate_lname(val):
    if not val.isalpha():
        raise ValueError("Last name must contain only letters.")
    return val

def validate_department(val):
    if len(val) != 3 or not val.isupper():
        raise ValueError("Department must be exactly 3 uppercase letters (e.g., HRM, FIN, OPS).")
    return val

def validate_phone(val):
    digits = "".join(filter(str.isdigit, val))
    if len(digits) != 10:
        raise ValueError("Phone must contain exactly 10 digits.")
    return digits

def validate_team_size(val):
    if not val.isdigit() or int(val) <= 0:
        raise ValueError("Team size must be a positive integer.")
    return int(val)


# --- Generic prompt with retry + cancel ---
def _prompt_with_cancel(label, validator, current=None):
    """Prompt for a field with retry logic. Allow q to cancel after first invalid."""
    first_attempt = True
    while True:
        base_label = f"{label}: " if first_attempt else f"{label} (or 'q' to cancel): "
        val = input(base_label).strip()
        if not first_attempt and val.lower() == "q":
            print(f"Cancelled updating {label}.")
            return None
        try:
            return validator(val)
        except Exception as e:
            print(f"Invalid input: {e}")
            first_attempt = False


# --- Employee creation flow ---
def _create_employee_flow():
    """Step-by-step creation with per-field validation."""

    is_manager = input("Is this a manager? (y/n): ").strip().lower() == "y"

    # Employee ID
    emp_id = input("Employee ID: ").strip()

    # First Name
    fname = _prompt_with_cancel("First Name", validate_fname)
    if fname is None:
        return None

    # Last Name
    lname = _prompt_with_cancel("Last Name", validate_lname)
    if lname is None:
        return None

    # Department
    department = _prompt_with_cancel("Department (3 uppercase letters)", validate_department)
    if department is None:
        return None

    # Phone
    phone = _prompt_with_cancel("Phone (10 digits)", validate_phone)
    if phone is None:
        return None

    # Manager field (optional, no cancel)
    if is_manager:
        while True:
            val = input("Team Size (integer): ").strip()
            try:
                team_size = validate_team_size(val)
                break
            except Exception as e:
                print(f"Invalid input: {e}")
        return Manager(emp_id, fname, lname, department, phone, team_size)

    return Employee(emp_id, fname, lname, department, phone)


# --- Employee editing flow ---
def _edit_employee_flow(emp):
    """Edit specific fields chosen by the user."""
    print("\nWhat would you like to edit?")
    print("1. First Name")
    print("2. Last Name")
    print("3. Department")
    print("4. Phone Number")
    if isinstance(emp, Manager):
        print("5. Team Size")

    choice = input("Enter numbers separated by commas (e.g., 1,3,4) or 'q' to cancel: ").strip()
    if choice.lower() == "q":
        print("Edit cancelled.")
        return

    selected = {c.strip() for c in choice.split(",")}

    if "1" in selected:
        fname = _prompt_with_cancel("First Name", validate_fname, emp.fname)
        if fname is not None:
            emp.fname = fname

    if "2" in selected:
        lname = _prompt_with_cancel("Last Name", validate_lname, emp.lname)
        if lname is not None:
            emp.lname = lname

    if "3" in selected:
        department = _prompt_with_cancel("Department (3 uppercase letters)", validate_department, emp.department)
        if department is not None:
            emp.department = department

    if "4" in selected:
        phone = _prompt_with_cancel("Phone (10 digits)", validate_phone, emp.phNumber)
        if phone is not None:
            emp.phNumber = phone

    if "5" in selected and isinstance(emp, Manager):
        team_size = _prompt_with_cancel("Team Size", validate_team_size, emp.team_size)
        if team_size is not None:
            emp.team_size = team_size


# --- Main loop ---
def main():
    employees = EmployeeData.load_employees()

    while True:
        EmployeeView.show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":  # Create
            emp = _create_employee_flow()
            if not emp:
                continue
            # ensure unique ID
            if any(e.id == emp.id for e in employees):
                EmployeeView.show_message("Error: An employee with that ID already exists.")
            else:
                employees.append(emp)
                EmployeeData.save_employees(employees)
                EmployeeView.show_message("Employee added successfully.")

        elif choice == "2":  # Edit
            emp_id = input("Enter Employee ID to edit: ").strip()
            emp = next((e for e in employees if e.id == emp_id), None)
            if not emp:
                EmployeeView.show_message("Employee not found.")
            else:
                _edit_employee_flow(emp)
                EmployeeData.save_employees(employees)
                EmployeeView.show_message("Employee updated successfully.")

        elif choice == "3":  # Delete
            emp_id = input("Enter Employee ID to delete: ").strip()
            before = len(employees)
            employees = [e for e in employees if e.id != emp_id]
            if len(employees) == before:
                EmployeeView.show_message("Employee not found.")
            else:
                EmployeeData.save_employees(employees)
                EmployeeView.show_message("Employee deleted successfully.")

        elif choice == "4":  # Display
            EmployeeView.show_employees(employees)

        elif choice == "5":  # Quit
            break

        else:
            EmployeeView.show_message("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
