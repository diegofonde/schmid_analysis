import pandas as pd
import numpy as np

def clean_raw_data(student_data):

    # Guard against empty lists
    if not student_data: 
        return []

    commuting_question = "How many minutes is your typical commute (one way)? *this includes walking, biking, driving, or public transit time"
    working_question = "How many hours per week do you typically work?"
    credits_question = "How many credits are you enrolled in this semester?"

    student_data_pd = pd.json_normalize(student_data)
    student_data_pd['questions.question_text'] = student_data_pd['questions.question_text'].astype(str) 
    student_data_pd['answer'] = student_data_pd['answer'].astype(str)

    # Cleaning for the commuting_question
    m_commute = student_data_pd['questions.question_text'] == commuting_question
    student_data_pd.loc[m_commute, 'clean_answer'] = np.where(
        student_data_pd.loc[m_commute, 'answer'] == '0-15 minutes', 
        'non-commuter', 
        'commuter'
    )

    # Cleaning for the working_question 
    m_work = student_data_pd['questions.question_text'] == working_question

    work_answers = student_data_pd.loc[m_work, 'answer'].fillna('').astype(str).str.strip().str.lower() # Check if the actual answers are empty, null, or 'nan'
    is_empty_or_null = work_answers.isin(['', 'nan', 'none', 'null'])

    student_data_pd.loc[m_work, 'clean_answer'] = np.where( # Assigns category based on whether or not the cell is empty
        is_empty_or_null, 
        'non-working', 
        'working'
    )

    # Cleaning for the credits_question
    m_credits = student_data_pd['questions.question_text'] == credits_question
    numeric_credits = pd.to_numeric(student_data_pd.loc[m_credits, 'answer'], errors='coerce')

    student_data_pd.loc[m_credits, 'clean_answer'] = pd.cut(
        numeric_credits,
        bins = [0, 11.9, 15.1, 18.1, 100],
        labels = ['1-11', '12-15', '16-18', '18+'] 
    ).astype(str)

    return student_data_pd[['answer_id', 'clean_answer']].to_dict(orient = 'records')

        





