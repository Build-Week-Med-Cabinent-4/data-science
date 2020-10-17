import logging
import random
from fastapi import APIRouter
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

log = logging.getLogger(__name__)
router = APIRouter()


# changed from relative to to full path

# model = pickle.load(open("nn_model.pkl", "rb"))
# transformer = pickle.load(open("transformer.pkl", "rb"))
strains = pd.read_csv("https://raw.githubusercontent.com/Build-Week-Med-Cabinent-4/data-science/main/data/clean/merged_dataset.csv")

transformer = TfidfVectorizer(stop_words="english", min_df=0.025, max_df=0.98, ngram_range=(1,3))
dtm = transformer.fit_transform(strains['lemmas'])
dtm = pd.DataFrame(dtm.todense(), columns=transformer.get_feature_names())
model = NearestNeighbors(n_neighbors=5, algorithm='kd_tree')
model.fit(dtm)

@router.post('/predict')
async def predict(request_text):
    """
    Predict the best strain of cannabis based on the parameters you define.
    This model will return what strain best suits the ailment you define.
    You can also select your favorite flavor and what effects you desire.
    """
    
    transformed = transformer.transform([request_text])
    dense = transformed.todense()
    recommendations = model.kneighbors(dense)[1][0]
    output_array = []
    for recommendation in recommendations:
        strain = strains.iloc[recommendation]
        output = strain.drop([
            'name', 'ailment', 'all_text', 'lemmas']).to_dict()
        output_array.append(output)
    return output_array

# from pydantic import BaseModel, Field, validator

# class Effects(BaseModel):
#     """Use this data model to parse the request body JSON."""

#     ailment: str = Field(..., example='insomnia')
#     flavor: str = Field(..., example='citrus')
#     effects: str = Field(..., example='relaxed')

#     def to_df(self):
#         """Convert pydantic object to pandas dataframe with 1 row."""
#         return pd.DataFrame([dict(self)])

    # @validator('x1')
    # def x1_must_be_positive(cls, value):
    #     """Validate that x1 is a positive number."""
    #     assert value > 0, f'x1 == {value}, must be > 0'
    #     return value

   

