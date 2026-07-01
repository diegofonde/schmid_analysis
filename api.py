# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np
import pandas as pd
import pickle
import gower

app = FastAPI(title = "PAM Clustering API") # Name of the API

# Allows for frontend and backend to communicate even with different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('pam_app_assets.pkl', 'rb') as f: # Opening pkl file containing 
    assets = pickle.load(f)

medoid_profiles = assets['medoid_profiles']
features = assets['features']

medoid_matrix = medoid_profiles[features].astype(object) # Makes sure that the code reads each column as the same type

class StudentFeatures(BaseModel): # Object for containing student features
    commuting_group: str
    work_group: str
    credits_bin: str
    labs: str

class StudentDataset(BaseModel):
    students: List[StudentFeatures]

@app.get("/") # Status returned when connected to the homepage
def home(): 
    return {"status": "API is online"}

@app.post("/predict") # When data is inputted by the user
def predict_group(dataset: StudentDataset):

    input_df = pd.DataFrame([s.model_dump() for s in dataset.students])

    credit_bin_order = ['1-11', '12-15', '16-18', '18+']
    labs_order = ['0', '1', '2', '3 or more']

    input_df['credits_bin'] = pd.Categorical(
        input_df['credits_bin'],
        categories = credit_bin_order,
        ordered = True
    )

    input_df['labs'] = pd.Categorical(
        input_df['labs'],
        categories = labs_order,
        ordered = True
    )

    input_df_gower = input_df[features].copy()
    input_df_gower['credits_bin'] = input_df_gower['credits_bin'].cat.codes
    input_df_gower['labs'] = input_df_gower['labs'].cat.codes

    medoid_matrix_ordered = medoid_matrix.copy()
    medoid_matrix_ordered['credits_bin'] = pd.Categorical(
        medoid_matrix_ordered['credits_bin'],
        categories = credit_bin_order,
        ordered = True
    )
    medoid_matrix_ordered['labs'] = pd.Categorical(
        medoid_matrix_ordered['labs'],
        categories = labs_order,
        ordered = True
    )

    medoid_matrix_ordered['credits_bin'] = medoid_matrix_ordered['credits_bin'].cat.codes
    medoid_matrix_ordered['labs'] = medoid_matrix_ordered['labs'].cat.codes

    is_category = [True, True, False, False]

    gower_matrix = gower.gower_matrix(input_df_gower,  medoid_matrix_ordered, cat_features= is_category) # Measures the distance of every row from the medoid

    assigned_indices = np.argmin(gower_matrix, axis = 1) # Returns 1D np array of the metroid the row is closest to

    results = []
    for idx in assigned_indices:
        results.append(
            {
                "group": int(medoid_profiles.iloc[idx]['group']),
                "group_name": str(medoid_profiles.iloc[idx]['group_name'])
            }
        )

    return {"Predictions": results}