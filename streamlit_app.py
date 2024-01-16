import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from src.utils import get_table_data, read_file
import streamlit as st
from src.mcq import generate_evaluate_chain
from src.logger import logging

with open('response.json','r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)

    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    #Add Button
    button=st.form_submit_button("Create MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                response=generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                            }
                    )
                quiz = response.get('quiz')
                if quiz is not None:
                     table_data = get_table_data(quiz)
                     if table_data is not None:
                          df = pd.DataFrame(table_data)
                          df.index = df.index + 1
                          st.table(df)
                          st.text_area(label='Review', value=response['review'])
            except Exception as e:
                 st.error(e)

