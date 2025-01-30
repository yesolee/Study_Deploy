from sqlalchemy import Column, Integer, String
from db import Base

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True)
    count = Column(Integer)
