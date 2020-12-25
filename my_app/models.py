from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, UniqueConstraint, CheckConstraint
from my_app.database import Base
from sqlalchemy.orm import mapper


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    average_rate = Column(Float, default=0)
    rates_sum = Column(Integer, default=0)
    rates_number = Column(Integer, default=0)
    UniqueConstraint(make, model)
