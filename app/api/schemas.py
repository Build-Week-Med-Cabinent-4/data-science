from pydantic import BaseModel

class Strains(BaseModel):
    ID: int
    Strain_Name: str
    Strain_Type: str
    Effect: str
    Ailment: str
    Flavor: str
    Description: str

    class Config:
        orm_mode = True

class InputsDB(BaseModel):
    ID: int
    Ailment_in: str
    Flavor_in: str
    Effects_in: str
    Strain_ID: int
    
    class Config:
        orm_mode = True
