import os
import logging
import random
from fastapi import APIRouter
from pydantic import BaseModel, Field, validator
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


log = logging.getLogger(__name__)
router = APIRouter()

# with open("../models/nn_model.pkl", "rb") as rf:
#     clf = pickle.load(rf)
# model = pickle.load(open("../../models/nn_model.pkl", "rb"))
# transformer = pickle.load(open("../../models/transformer.pkl", "rb"))
strains = pd.read_csv("https://raw.githubusercontent.com/Build-Week-Med-Cabinent-4/data-science/main/data/clean/merged_dataset.csv")
'''Needed to convert the Id column to a string type in order to display using 
 Fast API'''
strains['Id'] = strains['Id'].astype(str)

class Inputs(BaseModel):
    """Use this data model to parse the request body JSON."""

    ailment: str = Field(..., example="stress and insomnia")
    flavor = ''
    effects = ''

    def input_string(self):
        """Convert pydantic object to string to prep for model."""
        inputs = self.ailment + ' ' + self.flavor + ' ' + self.effects
        return inputs
    
    # @validator('ailment')
    # def ailment_must_have_val(cls, value):
    #     """Validate that ailment has a value inputted."""
    #     assert value != str, f'ailment == {value}, must have an input'
    #     return value


# Variables for predictive model.
transformer = TfidfVectorizer(stop_words="english", min_df=0.025,
                              max_df=0.98, ngram_range=(1,3))
dtm = transformer.fit_transform(strains['lemmas'])
dtm = pd.DataFrame(dtm.todense(), columns=transformer.get_feature_names())
model = NearestNeighbors(n_neighbors=5, algorithm='kd_tree')
model.fit(dtm)


@router.post('/predict')
async def predict(inputs: Inputs):
    """
    Predict the best strain of cannabis based on the parameters you define.
    
    This model will return what strain best suits your inputs.
    
    **Input:**
        
    * **ailment** : string (required) What is your ailment(s)?
    * **flavor** : string (optional) What flavor(s) do you like?
    * **effects** : string (optional) What effects do you desire?
    
    **Returns:**
    
    JSON file with the top 5 strains based on your inputs.
    
    For each strain you will get:
    * Strain Name
    * Type of Strain
    * Effect(s)
    * Flavor(s)
    * Description
    """
    
    transformed = transformer.transform([Inputs.input_string(inputs)])
    dense = transformed.todense()
    recommendations = model.kneighbors(dense)[1][0]
    output_array = []
    for recommendation in recommendations:
        strain = strains.iloc[recommendation]
        output = strain.drop([
            'name', 'ailment', 'all_text', 'lemmas']).to_dict()
        output_array.append(output)
    return output_array
