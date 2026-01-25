"""
Employee Management System
A Python program that manages employee records using a single class (EmployeeManager).
Features: Add, View, Update, Delete, Search employees with CSV persistence.

By: Nour
Under the supervision of Eng. Baraa
As part of the DEP Initiative
Date: January 2026



employee_management.py
│
├── 📦 Imports
│   ├── csv
│   ├── re
│   └── typing (Any, Dict, List, Optional, Tuple)
│
├── ✅ Validation Functions (Pure Functions)
│   ├── validate_email(email) → (bool, error)
│   ├── validate_salary(salary) → (bool, value, error)
│   ├── validate_required_field(value, field_name) → (bool, error)
│   └── validate_employee_id(emp_id, existing_ids) → (bool, error)
│
├── 🏢 Class: EmployeeManager
│   │
│   ├── 📊 Class Constants
│   │   └── FIELDNAMES = ['ID', 'Name', 'Position', 'Salary', 'Email']
│   │
│   ├── 🔨 Constructor
│   │   └── __init__(filename="employees.csv")
│   │       ├── self.filename
│   │       ├── self._employees (Dict)
│   │       └── calls _load_from_csv()
│   │
│   ├── 💾 CSV File Operations (Private Methods)
│   │   ├── _load_from_csv() → None
│   │   ├── _save_to_csv() → bool
│   │   └── _create_csv_file() → bool
│   │
│   ├── 🛠️ Helper Methods (Private)
│   │   ├── _prompt_until_valid(prompt, validator) → Any
│   │   └── _get_optional_input(prompt, current_value, validator) → Any
│   │
│   ├── 📋 CRUD Operations (Public Methods)
│   │   ├── 1️⃣ add_employee() → None
│   │   │   ├── Prompts: ID, Name, Position, Salary, Email
│   │   │   ├── Validates all inputs
│   │   │   ├── Stores in _employees dict
│   │   │   └── Saves to CSV
│   │   │
│   │   ├── 2️⃣ view_all_employees() → None
│   │   │   ├── Displays all employees in table format
│   │   │   └── Shows sorted by ID
│   │   │
│   │   ├── 3️⃣ update_employee() → None
│   │   │   ├── Search by ID
│   │   │   ├── Show current details
│   │   │   ├── Update fields (optional)
│   │   │   └── Save to CSV
│   │   │
│   │   ├── 4️⃣ delete_employee() → None
│   │   │   ├── Search by ID
│   │   │   ├── Confirmation prompt
│   │   │   ├── Delete from dict
│   │   │   └── Save to CSV
│   │   │
│   │   └── 5️⃣ search_employee() → None
│   │       ├── Search by ID
│   │       └── Display details or "not found"
│   │
│   └── 🚀 Main Method
│       └── run() → None
│           ├── Display menu (1-6)
│           ├── Get user choice
│           ├── Call corresponding method
│           └── Loop until exit (6)
│
└── 🎯 Main Execution
    └── if __name__ == "__main__":
        ├── Create EmployeeManager instance
        └── Call run()

📄 Data Flow:
┌─────────────────────────────────────────────────┐
│  User Input → Validation → _employees (Dict)    │
│       ↓                          ↓              │
│  Display ←─────────────→  employees.csv         │
└─────────────────────────────────────────────────┘
"""

import csv
import re
from typing import Any, Dict, List, Optional, Tuple


# ==================== Validation Functions ====================

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email format using regex."""
    if not email or not email.strip():
        return False, "Email cannot be empty"
    
    if not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()):
        return False, "Invalid email format"
    
    return True, None


def validate_salary(salary: str) -> Tuple[bool, Optional[float], Optional[str]]:
    """Validate that salary is a positive number."""
    if not salary or not salary.strip():
        return False, None, "Salary cannot be empty"
    
    try:
        salary_float = float(salary)
        if salary_float <= 0:
            return False, None, "Salary must be greater than 0"
        return True, salary_float, None
    except (ValueError, TypeError):
        return False, None, "Salary must be a valid number"


def validate_required_field(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
    """Validate that a required field is not empty."""
    if not value or not value.strip():
        return False, f"{field_name} cannot be empty"
    return True, None


def validate_employee_id(emp_id: str, existing_ids: List[str]) -> Tuple[bool, Optional[str]]:
    """Validate employee ID format and uniqueness."""
    if not emp_id or not emp_id.strip():
        return False, "Employee ID cannot be empty"
    
    if emp_id.strip() in existing_ids:
        return False, f"Employee with ID '{emp_id}' already exists"
    
    return True, None


def validate_unique_email(email: str, existing_emails: List[str]) -> Tuple[bool, Optional[str]]:
    """Validate email uniqueness."""
    is_valid, error = validate_email(email)
    if not is_valid:
        return False, error
    
    if email.strip() in existing_emails:
        return False, f"Email '{email}' is already registered to another employee"
    
    return True, None


# ==================== EmployeeManager Class ====================

class EmployeeManager:
    """
    Manages employee records with CRUD operations.
    Handles data storage (dict), CSV file operations, input validation, and CLI interface.
    """
    
    FIELDNAMES: List[str] = ['ID', 'Name', 'Position', 'Salary', 'Email']
    
    def __init__(self, filename: str = "employees.csv"):
        """Initialize the EmployeeManager."""
        self.filename = filename
        self._employees: Dict[str, Dict[str, Any]] = {}
        self._load_from_csv()
    
    # ==================== CSV File Operations ====================
    
    def _load_from_csv(self) -> None:
        """Load employee data from CSV file into dictionary."""
        self._employees = {}
        
        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row.get('ID'):
                        continue
                    
                    self._employees[row['ID']] = {
                        'ID': row['ID'],
                        'Name': row['Name'],
                        'Position': row['Position'],
                        'Salary': float(row['Salary']),
                        'Email': row['Email']
                    }
        except FileNotFoundError:
            self._create_csv_file()
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _save_to_csv(self) -> bool:
        """Save all employee data from dictionary to CSV file."""
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                # Sort employees by ID before writing to CSV
                for emp_id in sorted(self._employees.keys()):
                    writer.writerow(self._employees[emp_id])
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def _create_csv_file(self) -> bool:
        """Create an empty CSV file with headers."""
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
            return True
        except Exception:
            return False
    
    # ==================== Helper Methods ====================
    
    def _prompt_until_valid(self, prompt: str, validator) -> Any:
        """Prompt user until valid input is received."""
        while True:
            value = input(prompt).strip()
            result = validator(value)
            if result[0]:
                return result[1] if len(result) > 2 else value
            print(f"Error: {result[-1]}")
    
    def _get_optional_input(self, prompt: str, current_value: Any, validator) -> Any:
        """Get optional input from user with validation, keeping current value if blank."""
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                return current_value
            
            result = validator(user_input)
            if result[0]:
                return result[1] if len(result) > 2 else user_input
            print(f"Error: {result[-1]}")
    
    # ==================== CRUD Operations ====================
    
    def add_employee(self) -> None:
        """Add a new employee to the system."""
        print("\n" + "="*50)
        print("ADD NEW EMPLOYEE")
        print("="*50)
        
        emp_id = self._prompt_until_valid(
            "Enter Employee ID: ",
            lambda v: validate_employee_id(v, list(self._employees.keys()))
        )
        
        name = self._prompt_until_valid(
            "Enter Name: ",
            lambda v: validate_required_field(v, "Name")
        )
        
        position = self._prompt_until_valid(
            "Enter Position: ",
            lambda v: validate_required_field(v, "Position")
        )
        
        salary = self._prompt_until_valid(
            "Enter Salary: ",
            validate_salary
        )
        
        # Get list of existing emails
        existing_emails = [emp['Email'] for emp in self._employees.values()]
        
        email = self._prompt_until_valid(
            "Enter Email: ",
            lambda v: validate_unique_email(v, existing_emails)
        )
        
        self._employees[emp_id] = {
            'ID': emp_id,
            'Name': name,
            'Position': position,
            'Salary': salary,
            'Email': email
        }
        
        self._save_to_csv()
        print(f"\nEmployee '{name}' added successfully!")
        input("\nPress Enter to continue...")
    
    def view_all_employees(self) -> None:
        """Display all employees in a readable format."""
        print("\n" + "="*60)
        print("ALL EMPLOYEES")
        print("="*60)
        
        if not self._employees:
            print("\nNo employees found in the system.")
            print("Please add some employees first.")
        else:
            print(f"\n{'ID':<10} {'Name':<25} {'Position':<20} {'Salary':<15} {'Email':<30}")
            print("-" * 100)
            
            for employee in self._employees.values():
                print(f"{employee['ID']:<10} {employee['Name']:<25} {employee['Position']:<20} "
                      f"${employee['Salary']:>12,.2f}   {employee['Email']:<30}")
            
            print("-" * 100)
            print(f"Total Employees: {len(self._employees)}")
        
        input("\nPress Enter to continue...")
    
    def update_employee(self) -> None:
        """Update an existing employee's details by ID."""
        print("\n" + "="*50)
        print("UPDATE EMPLOYEE")
        print("="*50)
        
        if not self._employees:
            print("\nNo employees in the system. Please add employees first.")
            input("\nPress Enter to continue...")
            return
        
        emp_id = input("Enter Employee ID to update: ").strip()
        
        if emp_id not in self._employees:
            print(f"\nEmployee with ID '{emp_id}' not found!")
            input("\nPress Enter to continue...")
            return
        
        employee = self._employees[emp_id]
        
        print(f"\nCurrent Details:")
        print(f"  Name: {employee['Name']}")
        print(f"  Position: {employee['Position']}")
        print(f"  Salary: ${employee['Salary']:,.2f}")
        print(f"  Email: {employee['Email']}")
        print("\nLeave fields blank to keep current values:")
        
        name = self._get_optional_input(
            f"Enter new Name (current: {employee['Name']}): ",
            employee['Name'],
            lambda v: validate_required_field(v, "Name")
        )
        
        position = self._get_optional_input(
            f"Enter new Position (current: {employee['Position']}): ",
            employee['Position'],
            lambda v: validate_required_field(v, "Position")
        )
        
        salary = self._get_optional_input(
            f"Enter new Salary (current: ${employee['Salary']:,.2f}): ",
            employee['Salary'],
            validate_salary
        )
        
        # Get list of existing emails excluding current employee's email
        existing_emails = [emp['Email'] for emp_id_key, emp in self._employees.items() if emp_id_key != emp_id]
        
        email = self._get_optional_input(
            f"Enter new Email (current: {employee['Email']}): ",
            employee['Email'],
            lambda v: validate_unique_email(v, existing_emails)
        )
        
        self._employees[emp_id] = {
            'ID': emp_id,
            'Name': name,
            'Position': position,
            'Salary': salary,
            'Email': email
        }
        
        self._save_to_csv()
        print(f"\nEmployee with ID '{emp_id}' updated successfully!")
        input("\nPress Enter to continue...")
    
    def delete_employee(self) -> None:
        """Delete an employee from the system by ID."""
        print("\n" + "="*50)
        print("DELETE EMPLOYEE")
        print("="*50)
        
        if not self._employees:
            print("\nNo employees in the system. Please add employees first.")
            input("\nPress Enter to continue...")
            return
        
        emp_id = input("Enter Employee ID to delete: ").strip()
        
        if emp_id not in self._employees:
            print(f"\nEmployee with ID '{emp_id}' not found!")
            input("\nPress Enter to continue...")
            return
        
        employee = self._employees[emp_id]
        
        print(f"\nAre you sure you want to delete this employee?")
        print(f"  Name: {employee['Name']}")
        print(f"  Position: {employee['Position']}")
        print(f"  Email: {employee['Email']}")
        
        confirm = input("\nType 'YES' to confirm deletion: ").strip().upper()
        
        if confirm == 'YES':
            del self._employees[emp_id]
            self._save_to_csv()
            print(f"\nEmployee with ID '{emp_id}' deleted successfully!")
        else:
            print("\nDeletion cancelled.")
        
        input("\nPress Enter to continue...")
    
    def search_employee(self) -> None:
        """Search and display an employee's details by their unique ID."""
        print("\n" + "="*50)
        print("SEARCH EMPLOYEE")
        print("="*50)
        
        if not self._employees:
            print("\nNo employees in the system. Please add employees first.")
            input("\nPress Enter to continue...")
            return
        
        emp_id = input("Enter Employee ID to search: ").strip()
        
        if emp_id not in self._employees:
            print(f"\nEmployee with ID '{emp_id}' not found!")
        else:
            employee = self._employees[emp_id]
            print("\n" + "-"*40)
            print("EMPLOYEE FOUND:")
            print("-"*40)
            print(f"  ID:       {employee['ID']}")
            print(f"  Name:     {employee['Name']}")
            print(f"  Position: {employee['Position']}")
            print(f"  Salary:   ${employee['Salary']:,.2f}")
            print(f"  Email:    {employee['Email']}")
            print("-"*40)
        
        input("\nPress Enter to continue...")
    
    # ==================== Main Run Method ====================
    
    def run(self) -> None:
        """Main method to run the employee management system."""
        while True:
            print("\n" + "="*60)
            print("    WELCOME TO EMPLOYEE MANAGEMENT SYSTEM")
            print("="*60)
            print("\nMain Menu:")
            print("  1. Add Employee")
            print("  2. View All Employees")
            print("  3. Update Employee")
            print("  4. Delete Employee")
            print("  5. Search Employee")
            print("  6. Exit")
            print("\n" + "-"*60)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_all_employees()
            elif choice == '3':
                self.update_employee()
            elif choice == '4':
                self.delete_employee()
            elif choice == '5':
                self.search_employee()
            elif choice == '6':
                print("\n" + "="*60)
                print("  Thank you for using Employee Management System!")
                print("  Goodbye!, With Nour Regards")
                print("="*60)
                break
            else:
                print("\nInvalid choice! Please enter a number between 1 and 6.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    manager = EmployeeManager()
    manager.run()