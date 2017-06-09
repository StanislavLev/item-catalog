import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Dealers(Base):
    __tablename__ = 'dealers_db'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    
 
class Cars(Base):
    __tablename__ = 'cars_db'

    id = Column(Integer, primary_key = True)
    created = Column(DateTime, nullable=False)
    newCar = Column(Boolean, nullable=False)
    type = Column(String(100), nullable=False)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    trim = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(500))
    picture = Column(String(300))
    dealer_id = Column(Integer,ForeignKey('dealers_db.id'))
    dealer = relationship('Dealers') 
 
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'created' : self.created.isoformat(),
            'newCar' : self.newCar,
            'type' : self.type,
            'make' : self.make,
            'model' : self.model,
            'trim' : self.trim,
            'year' : self.year,
            'mileage' : self.mileage,
            'price' : self.price,
            'description' : self.description,
            'dealer_id' : self.dealer_id,
        }

engine = create_engine('sqlite:///cars4sale.db')
Base.metadata.create_all(engine)