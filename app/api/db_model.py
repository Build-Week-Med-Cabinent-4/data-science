import os
from os import getenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import Date
from app.database import Base


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, bind=engine)

Base = declarative_base()

class Strains(Base):
    
    __tablename__ = 'strains'
    
    id = Column(Integer, primary_key=True)
    strain_name = Column(String(55), nullable=False)
    strain_type = Column(String(55))
    description = Column(String)
    
    effects = relationship('Effects', back_populates='strains')
    inputs = relationship('InputsDB', back_populates='strains')    
    
class Effects(Base):
    
    __tablename__ = 'effects'
    
    id = Column(Integer, primary_key=True)
    effect = Column(String)
    ailment = Column(String)
    flavor = Column(String)
    strain_id = Column(Integer, ForeignKey('strains.id'), nullable=False)
    
    strains = relationship('Strains', back_populates='effects', lazy=True)

class InputsDB(Base):
    
    __tablename__ = 'inputs_db'
    
    id = Column(Integer, primary_key=True)
    ailment_in = Column(String, nullable=False)
    flavor_in = Column(String)
    effects_in = Column(String)
    strain_id = Column(Integer, ForeignKey('strains.id'), nullable=False)
    
    strains = relationship('Strains', back_populates='inputs', lazy=True)
