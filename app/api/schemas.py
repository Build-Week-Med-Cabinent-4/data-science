from pydantic import BaseModel

class Strains(BaseModel):
    id: int
    strain_name: str
    strain_type: str
    description: str

    class Config:
        orm_mode = True

class Effects(BaseModel):
    id: int
    effect: str
    ailment: str
    flavor: str
    strain_id: int
    
    class Config:
        orm_mode = True

class InputsDB(BaseModel):
    id: int
    ailment_in: str
    flavor_in: str
    effects_in: str
    strain_id: int
    
    class Config:
        orm_mode = True