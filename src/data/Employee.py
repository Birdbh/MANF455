from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data.DatabaseConnector import Base, engine, Session

class Employee(Base):
    __tablename__ = 'employee'

    employeeId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum('Manager', 'Technician', 'Operator', name='role_types'), nullable=False)

class EmployeeTable:
    def __init__(self):
        self.engine = engine
        self.Session = Session
        self.create_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_employee(self, name: str, username: str, password: str, role: str):
        session = self.Session()
        new_employee = Employee(name=name, username=username, password=password, role=role)
        session.add(new_employee)
        session.commit()
        session.close()

    def get_all_employees(self):
        session = self.Session()
        employees = session.query(Employee).all()
        session.close()
        return employees

    def get_all_operators(self):
        session = self.Session()
        operators = session.query(Employee).filter(Employee.role == "Operator").all()
        session.close()
        return operators

    def authenticate_employee_details(self, username, password):
        session = self.Session()
        employee = session.query(Employee.employeeId, Employee.name, Employee.role).filter(
            Employee.username == username,
            Employee.password == password
        ).first()
        session.close()
        return employee

    def get_employee_details(self):
        session = self.Session()
        employees = session.query(Employee.employeeId, Employee.name, Employee.role).all()
        session.close()
        return employees