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
