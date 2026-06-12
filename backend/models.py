from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    ngo_name = Column(String, nullable=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    food_item = Column(String)
    quantity = Column(String)
    pickup_time = Column(String)
    status = Column(String, default="Pending")
    otp = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)