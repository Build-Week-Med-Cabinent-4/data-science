import os
from os import getenv
from typing import List
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from . import schemas


router = APIRouter()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, bind=engine)

Base = declarative_base()


class Strains(Base):

    __tablename__ = 'strains'

    ID = Column(Integer, primary_key=True)
    Strain_Name = Column(String(55), nullable=False)
    Strain_Type = Column(String(55))
    Description = Column(String)
    Effect = Column(String)
    Ailment = Column(String)
    Flavor = Column(String)


class InputsDB(Base):

    __tablename__ = 'inputs_db'

    ID = Column(Integer, primary_key=True)
    Ailment_In = Column(String, nullable=False)
    Flavor_In = Column(String)
    Effects_In = Column(String)

db = SessionLocal()

if not engine.dialect.has_table(engine, 'strains'):
    Base.metadata.create_all(bind=engine)

'''Needed to comment out the code below after creating the database with
the static csv dataset to prevent duplication. This part of the function
will need to be researched more to find a better option.'''
# url = 'https://raw.githubusercontent.com/Build-Week-Med-Cabinent-4/data-science/main/data/clean/merged_dataset.csv'

# df = pd.read_csv(url)
# data = df.to_dict()

# for _,row in df.iterrows():

#     strains_db = Strains(
#         Strain_Name=row['Strain'],
#         Strain_Type=row['Type'],
#         Effect=row['Effects'],
#         Ailment=row['ailment'],
#         Flavor=row['Flavor'],
#         Description=row['Description']
#     )
#     db.add(strains_db)

# db.commit()


def get_db():
    '''This function will return the data from database.'''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Set the route for the strains table
@router.get('/strains', response_model=List[schemas.Strains])
async def show_strains(db: Session=Depends(get_db)):
    '''
    View the strain table information we have in our database.

    Features in this table include:
    * **ID**: The id number assigned to the strain (Primary Key)
    * **Strain_Name**: The name of the strain
    * **Strain_Type**: The type of strain
    * **Effect**: What kind of effect(s) know for the strain
    * **Ailment**: What ailment(s) the strain is known for helping
    * **Flavor**: A description of the flavor associated with the strain
    * **Description**: Describes the strain
    '''
    strains = db.query(Strains).all()
    return strains
