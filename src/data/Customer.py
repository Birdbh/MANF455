from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data.DatabaseConnector import Base, engine, Session

class Customer(Base):
    __tablename__ = 'customer'

    customerid = Column(Integer, primary_key=True, autoincrement=True)
    customername = Column(String, nullable=False)
    customeremail = Column(String, nullable=False)
    customeraddress = Column(String, nullable=False)

class CustomerTable:
    def __init__(self):
        self.engine = engine
        self.Session = Session
        self.create_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_customer(self, customername: str, customeremail: str, customeraddress: str):
        session = self.Session()
        new_customer = Customer(customername=customername, customeremail=customeremail, customeraddress=customeraddress)
        session.add(new_customer)
        session.commit()
        session.close()

    def get_all_customers(self):
        session = self.Session()
        customers = session.query(Customer).all()
        session.close()
        return customers
    
    def get_customer_name_by_id(self, customerid: int):
        session = self.Session()
        customer = session.query(Customer).filter_by(customerid=customerid).first()
        session.close()
        return customer.customername if customer else None
    
    def get_customer_email_by_id(self, customerid: int):
        session = self.Session()
        customer = session.query(Customer).filter_by(customerid=customerid).first()
        session.close()
        return customer.customeremail if customer else None
    
    def get_customer_address_by_id(self, customerid: int):
        session = self.Session()
        customer = session.query(Customer).filter_by(customerid=customerid).first()
        session.close()
        return customer.customeraddress if customer else None
    
    def remove_customer(self, customerid: int):
        session = self.Session()
        customer = session.query(Customer).filter_by(customerid=customerid).first()
        if customer:
            session.delete(customer)
            session.commit()
        session.close()