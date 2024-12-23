from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DiceRoll(Base):
    __tablename__ = 'dice_rolls'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_1 = Column(Integer, nullable=False)
    roll_2 = Column(Integer, nullable=False)
    roll_3 = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)

