import csv
from app.api import db_model
from app.database import SessionLocal, engine

db = SessionLocal()

db_model.Base.metadata.create_all(bind=engine)

url = 'https://raw.githubusercontent.com/Build-Week-Med-Cabinent-4/data-science/main/data/clean/merged_dataset.csv'

with open(url, 'r') as f:
    csv_reader = csv.DictReader(f)
    
    for row in csv_reader:
        
        strains_db = db_model.Strains(
            strain_name=row['Strain'],
            strain_type=row['Type'],
            description=row['Description']
        )
        db.add(strains_db)
        
        effects_db = db_model.Effects(
            effect=row['Effects'],
            ailment=row['ailment'],
            flavor=row['Flavor']
        )
        db.add(effects_db)
        
    db.commit()
    
db.close()