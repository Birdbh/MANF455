from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data import DatabaseConnector
import datetime

Base = declarative_base()

class Downtime(Base):
    __tablename__ = 'downtime'

    downtimeId = Column(Integer, primary_key=True, autoincrement=True)
    employeeId = Column(Integer, nullable=False)
    downtimeReason = Column(Enum("Machine Fault", "Product Malfunction", "Labour Incident", name="downtime_reason_types"), nullable=False)
    downtimeStart = Column(DateTime, nullable=False)
    downtimeEnd = Column(DateTime, nullable=True)
    downtimeDelta = Column(Interval, nullable=True)
    status = Column(Enum("Pending", "Resolved", name="status_types"), nullable=False)

class DowntimeTable:
    def __init__(self):
        self.engine = create_engine("sqlite:///MESDATABASE")
        self.Session = sessionmaker(bind=self.engine)
        self.create_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_downtime(self, employeeId: int, downtimeReason: str):
        session = self.Session()
        current_time = datetime.datetime.now()
        new_downtime = Downtime(employeeId=employeeId, downtimeReason=downtimeReason, status='Pending', downtimeStart=current_time)
        session.add(new_downtime)
        session.commit()
        session.close()

    def get_last_row(self):
        session = self.Session()
        try:
            last_downtime = session.query(Downtime).order_by(Downtime.downtimeId.desc()).first()
            session.close()
            return last_downtime
        except:
            session.close()
            return None

    def is_currently_downtime(self):
        return self.get_last_row_status() == 'Pending'

    def get_last_row_status(self):
        last_downtime = self.get_last_row()
        return last_downtime.status if last_downtime else None

    def get_last_row_reason(self):
        last_downtime = self.get_last_row()
        return last_downtime.downtimeReason if last_downtime else None

    def end_downtime(self):
        session = self.Session()
        last_downtime = session.query(Downtime).order_by(Downtime.downtimeId.desc()).first()
        if last_downtime:
            last_downtime.downtimeEnd = datetime.datetime.now()
            last_downtime.downtimeDelta = last_downtime.downtimeEnd - last_downtime.downtimeStart
            last_downtime.status = 'Resolved'
            session.commit()
        session.close()