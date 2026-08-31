import pandas as pd
import numpy as np

def clean_model_data(df):

    commuting_question = "How many minutes is your typical commute (one way)? *this includes walking, biking, driving, or public transit time"
    working_question = "How many hours per week do you typically work?"
    credits_question = "How many credits are you enrolled in this semester?"
    labs_question = "How many lab courses are you enrolled in this semester?"

    