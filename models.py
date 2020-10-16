import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


# changed from relative to to full path
model = pickle.load(open("../models/nearest_neighbors_model.sav", "rb"))
transformer = pickle.load(open("../models/transformer.sav", "rb"))
strains = pd.read_csv("../data/clean/merged_dataset.csv")


def predict(request_text):
    transformed = transformer.transform([request_text])
    dense = transformed.todense()
    recommendations = model.kneighbors(dense)[1][0][0]
    output_array = []
    for recommendation in recommendations:
        strain = strains.iloc[recommendation]
        output = strain.drop([
            'name', 'ailment', 'all_text', 'lemmas']).to_dict()
        output_array.append(output)
    return output_array
