'''
This main code of the API. 
'''
from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from app.api import predict
from app.api import db_model, schemas
from app.database import SessionLocal, engine
from . import csv_to_db


# Create an app instance
app = FastAPI(
    title='Cannabis Strains',
    description='API to predict best strain of cannabis based on selected parameters.',
    version='0.1',
    docs_url='/',
)

# Create the database
db_model.Base.metadata.create_all(bind=engine)

# Create the route for the predictions
app.include_router(predict.router)

# Origins allowed for CORSMiddleware
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

# Set the parameters for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_db():
    '''This function will return the data from database.'''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Set the route for the strains table
@app.get('/strains', response_model=List[schemas.Strains])
async def show_strains(db: Session = Depends(get_db)):
    '''
    View the strain table information we have in our database.
    
    Features in this table include:
    * **id**: The id number assigned to the strain (Primary Key)
    * **strain_name**: The name of the strain
    * **strain_type**: The type of strain
    * **description**: Describes the strain
    '''
    strains = db.query(db_model.Strains).all()
    return strains

# Set the route for the effects table
@app.get('/effects', response_model=List[schemas.Effects])
async def show_effects(db: Session = Depends(get_db)):
    '''
    View the effects table information we have in our database.
    
    Features in this table include:
    * **id**: The id number assigned to the effects (Primary Key)
    * **effect**: What kind of effect(s) know for the strain
    * **ailment**: What ailment(s) the strain is known for helping
    * **flavor**: A description of the flavor associated with the strain
    * **strain_id**: Connects the strain id to the strain table's id
    '''
    effects = db.query(db_model.Effects).all()
    return effects

# Allows running the app locally
if __name__ == '__main__':
    uvicorn.run(app)
