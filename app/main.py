'''
This main code of the API. 
'''
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from app.api import predict
from app.api import db_model, schemas


description = """
API to predict best strain of cannabis based on selected parameters.

<img src="https://thumbs.dreamstime.com/b/marijuana-panorama-farm-field-green-65019611.jpg" width="70%" />

This API utilizes a K Nearest Neighbors model for the prediction function.
"""

# Create an app instance
app = FastAPI(
    title='Cannabis Strains',
    description=description,
    version='0.1',
    docs_url='/',
)

# Connect the routes
app.include_router(predict.router)
app.include_router(db_model.router)

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


# Allows running the app locally
if __name__ == '__main__':
    uvicorn.run(app)
