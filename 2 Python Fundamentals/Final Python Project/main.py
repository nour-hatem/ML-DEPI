"""
Employee Data Management System - Main Entry Point
A Python program that manages employee records using a single class (EmployeeManager).
"""

from employee_manager import EmployeeManager


def main():
    """
    Main function to start the Employee Management System.
    """
  
    manager = EmployeeManager()
    manager.run()


if __name__ == "__main__":
    main()

