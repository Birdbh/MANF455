from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

#TODO: need to add a foreign key constraint for customer_id

class Order(Base):
    __tablename__ = 'orders'

    orderId = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    drilling_operation = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    passQualityControl = Column(Boolean, nullable=False)

class OrderTable:
    def __init__(self):
        self.engine = create_engine("sqlite:///MESDATABASE")
        self.Session = sessionmaker(bind=self.engine)
        self.create_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_order(self, customer_id: int, drilling_operation: int, order_date: str, status: str, passQualityControl: bool):
        session = self.Session()
        new_order = Order(
            customer_id=customer_id,
            drilling_operation=drilling_operation,
            order_date=datetime.datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S'),
            status=status,
            passQualityControl=passQualityControl
        )
        session.add(new_order)
        session.commit()
        session.close()

    def get_all_orders(self):
        session = self.Session()
        orders = session.query(Order).all()
        session.close()
        return orders

    def get_last_row_id(self):
        session = self.Session()
        last_order = session.query(Order).order_by(Order.orderId.desc()).first()
        session.close()
        return last_order.orderId if last_order else None

    def update_drilling_operation(self, order_id: int, new_drilling_operation: int):
        session = self.Session()
        order = session.query(Order).filter_by(orderId=order_id).first()
        if order:
            order.drilling_operation = new_drilling_operation
            session.commit()
        session.close()

    def update_start_time(self, order_id: int, new_start_time: str):
        session = self.Session()
        order = session.query(Order).filter_by(orderId=order_id).first()
        if order:
            order.order_date = datetime.datetime.strptime(new_start_time, '%Y-%m-%d %H:%M:%S')
            session.commit()
        session.close()

    #TODO: This method still needs to be called by the Queue
    def set_status_completed(self, order_id: int):
        session = self.Session()
        order = session.query(Order).filter_by(orderId=order_id).first()
        if order:
            order.status = "Completed"
            session.commit()
        session.close()

    def update_pass_quality_control(self, order_id: int, new_pass_quality_control: bool):
        session = self.Session()
        order = session.query(Order).filter_by(orderId=order_id).first()
        if order:
            order.passQualityControl = new_pass_quality_control
            session.commit()
        session.close()

    def get_total_parts_produced_for_date(self, date):
        session = self.Session()
        date_next_day = date + datetime.timedelta(days=1)
        total_parts_produced = session.query(Order).filter(
            Order.order_date >= date,
            Order.order_date <= date_next_day,
            Order.status == "Completed",
        ).count()
        session.close()
        return total_parts_produced
    
    def get_total_good_parts_produced_today(self, date):
        session = self.Session()
        date_next_day = date + datetime.timedelta(days=1)
        total_good_parts_produced = session.query(Order).filter(
            Order.order_date >= date,
            Order.order_date <= date_next_day,
            Order.status == "Completed",
            Order.passQualityControl == True
        ).count()
        session.close()
        return total_good_parts_produced