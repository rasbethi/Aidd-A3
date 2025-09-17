# employee.py
import re
import logging

# Log validation errors from model
logging.basicConfig(
    filename="employee_test.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

_NAME_HAS_DIGIT = re.compile(r"\d")
_DEPT_PATTERN = re.compile(r"^[A-Z]{3}$")  # exactly 3 uppercase letters


class Employee:
    """Core employee model with strict validation via properties."""
    def __init__(self, emp_id: str, fname: str, lname: str, department: str, phNumber: str):
        emp_id = (emp_id or "").strip()
        if not emp_id:
            self._log_error("Empty employee id")
            raise ValueError("Employee id cannot be empty.")
        self._id = emp_id  # read-only after creation

        self.fname = fname
        self.lname = lname
        self.department = department
        self.phNumber = phNumber

    # read-only id
    @property
    def id(self) -> str:
        return self._id

    # fname
    @property
    def fname(self) -> str:
        return self._fname

    @fname.setter
    def fname(self, value: str) -> None:
        v = (value or "").strip()
        if not v or _NAME_HAS_DIGIT.search(v):
            self._log_error(f"Invalid first name: {value!r}")
            raise ValueError("First name cannot be empty or contain digits.")
        self._fname = v.title()

    # lname
    @property
    def lname(self) -> str:
        return self._lname

    @lname.setter
    def lname(self, value: str) -> None:
        v = (value or "").strip()
        if not v or _NAME_HAS_DIGIT.search(v):
            self._log_error(f"Invalid last name: {value!r}")
            raise ValueError("Last name cannot be empty or contain digits.")
        self._lname = v.title()

    # department (normalize to uppercase, exactly 3 letters)
    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        v = (value or "").strip().upper()
        if not _DEPT_PATTERN.match(v):
            self._log_error(f"Invalid department code: {value!r}")
            raise ValueError("Department must be exactly 3 uppercase letters (e.g., HRM, FIN, OPS).")
        self._department = v

    # phone number (stored as 10 digits, accepts formatted input)
    @property
    def phNumber(self) -> str:
        return self._phNumber

    @phNumber.setter
    def phNumber(self, value: str) -> None:
        digits = re.sub(r"\D", "", str(value or ""))
        if len(digits) != 10:
            self._log_error(f"Invalid phone number: {value!r}")
            raise ValueError("Phone number must contain exactly 10 digits (formats allowed; will be sanitized).")
        self._phNumber = digits

    def getphNumber(self) -> str:
        """Return the stored unformatted 10-digit phone number."""
        return self._phNumber

    def __str__(self) -> str:
        return f"[{self.id}] {self.fname} {self.lname} | Dept: {self.department} | Phone: {self._phNumber}"

    def _log_error(self, msg: str) -> None:
        logging.error(msg)


class Manager(Employee):
    """Manager subclass with extra attribute and polymorphic __str__."""
    def __init__(self, emp_id: str, fname: str, lname: str, department: str, phNumber: str, team_size):
        super().__init__(emp_id, fname, lname, department, phNumber)
        self.team_size = team_size  # validate in property

    @property
    def team_size(self) -> int:
        return self._team_size

    @team_size.setter
    def team_size(self, value) -> None:
        try:
            n = int(value)
        except Exception:
            self._log_error(f"Invalid team_size (not int): {value!r}")
            raise ValueError("Team size must be an integer.")
        if n < 0:
            self._log_error(f"Invalid team_size (negative): {value!r}")
            raise ValueError("Team size cannot be negative.")
        self._team_size = n

    def __str__(self) -> str:
        return (f"[{self.id}] {self.fname} {self.lname} "
                f"(Manager, Team Size: {self.team_size}) | Dept: {self.department} | Phone: {self.getphNumber()}")


# Demo for Part 5 — safe to run directly; does NOT import app/data/view
if __name__ == "__main__":
    cases = [
        ("E001", "Alice", "Johnson", "HRM", "123-456-7890"),
        ("E002", "Bob", "Smith", "fin", "987.654.3210"),  # dept auto-normalizes to FIN
        ("E_BAD", "Al1ce", "Smith", "FIN", "1234567890"),  # bad fname
        ("E003", "Carol", "Brown", "ENG", "555-12"),       # bad phone
    ]
    for c in cases:
        try:
            print(Employee(*c))
        except Exception as e:
            print("ERROR:", e)

    try:
        print(Manager("M001", "Eve", "Clark", "OPS", "(111) 222-3333", 10))
        print(Manager("M002", "Ray", "Ng", "ENG", "2223334444", -1))  # bad team_size
    except Exception as e:
        print("ERROR:", e)
