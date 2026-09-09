import pandas as pd
import numpy as np

def clean_model_data(connection):

    commuting_question = "How many minutes is your typical commute (one way)? *this includes walking, biking, driving, or public transit time"
    working_question = "How many hours per week do you typically work?"
    credits_question = "How many credits are you enrolled in this semester?"
    labs_question = "How many lab courses are you enrolled in this semester?"

    question_list = [commuting_question, working_question, credits_question, labs_question]

    response = (
        connection.table("answers")
        .select("*")
    )





